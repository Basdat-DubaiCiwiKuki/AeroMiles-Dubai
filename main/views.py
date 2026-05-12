import re
import hashlib
from datetime import date, datetime

from django.shortcuts import render, redirect
from django.db import connection, transaction
from django.db.utils import ProgrammingError


# ─── HELPERS ──────────────────────────────────────────────────────────────────

def hash_password(plain: str) -> str:
    """SHA-256 hex digest — same algorithm used in SQL dump."""
    return hashlib.sha256(plain.encode()).hexdigest()


SALUTATIONS = {'Mr.', 'Mrs.', 'Ms.', 'Dr.'}
CABIN_CLASSES = {'Economy', 'Business', 'First'}
CLAIM_STATUSES = {'Menunggu', 'Disetujui', 'Ditolak'}


def normalize_email(email: str) -> str:
    return (email or '').strip().lower()


def _parse_date(value, label):
    try:
        return datetime.strptime(value, "%Y-%m-%d").date(), None
    except (TypeError, ValueError):
        return None, f'Format {label} tidak valid.'


def _validate_max_length(value, max_length, label):
    if len(value) > max_length:
        return f'{label} maksimal {max_length} karakter.'
    return None


def _validate_positive_int(value, label):
    try:
        parsed = int(value)
        if parsed < 1:
            raise ValueError
        return parsed, None
    except (TypeError, ValueError):
        return None, f'{label} harus berupa angka positif.'


def _row_exists(cur, table, column, value):
    cur.execute(f"SELECT 1 FROM {table} WHERE {column} = %s", [value])
    return cur.fetchone() is not None


def _fetch_identity_types(cur):
    try:
        cur.execute("SELECT nama FROM jenis_identitas ORDER BY urutan, nama")
    except ProgrammingError:
        connection.rollback()
        _create_identity_type_lookup_from_identitas()
        cur.execute("SELECT nama FROM jenis_identitas ORDER BY urutan, nama")
    return [row[0] for row in cur.fetchall()]


def _identity_type_exists(jenis):
    with connection.cursor() as cur:
        try:
            cur.execute("SELECT 1 FROM jenis_identitas WHERE nama = %s", [jenis])
        except ProgrammingError:
            connection.rollback()
            _create_identity_type_lookup_from_identitas()
            cur.execute("SELECT 1 FROM jenis_identitas WHERE nama = %s", [jenis])
        return cur.fetchone() is not None


def _create_identity_type_lookup_from_identitas():
    with connection.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS jenis_identitas (
                nama VARCHAR(30) PRIMARY KEY,
                urutan INT NOT NULL UNIQUE
            )
        """)
        cur.execute("""
            INSERT INTO jenis_identitas (nama, urutan)
            SELECT jenis, ROW_NUMBER() OVER (ORDER BY MIN(nomor)) AS urutan
            FROM identitas
            GROUP BY jenis
            ON CONFLICT (nama) DO NOTHING
        """)


def _validate_identity_dates(tanggal_terbit, tanggal_habis):
    terbit, err = _parse_date(tanggal_terbit, 'tanggal terbit')
    if err:
        return None, None, err
    habis, err = _parse_date(tanggal_habis, 'tanggal habis')
    if err:
        return None, None, err
    if terbit >= habis:
        return None, None, 'Tanggal terbit harus lebih awal dari tanggal habis.'
    return terbit, habis, None


def _dashboard_activity(tipe, jumlah, timestamp):
    is_credit = jumlah > 0
    label = {
        'Transfer Keluar': 'Transfer',
        'Transfer Masuk': 'Transfer',
        'Redeem': 'Redeem',
        'Beli Package': 'Package',
        'Klaim Disetujui': 'Klaim',
    }.get(tipe, tipe)

    if tipe == 'Redeem':
        color = 'orange'
    elif is_credit:
        color = 'emerald' if tipe == 'Beli Package' else 'blue'
    else:
        color = 'red'

    return {
        'tipe': tipe,
        'label': label,
        'jumlah': abs(jumlah),
        'signed_jumlah': jumlah,
        'timestamp': timestamp,
        'is_credit': is_credit,
        'icon_color': color,
    }


def validate_profil_data(data):
    salutation      = data.get('salutation', '').strip()
    first_name      = data.get('first_name', '').strip()
    middle_name     = data.get('middle_name', '').strip()
    last_name       = data.get('last_name', '').strip()
    kewarganegaraan = data.get('kewarganegaraan', '').strip()
    country_code    = data.get('country_code', '').strip()
    mobile_number   = data.get('mobile_number', '').strip()
    tanggal_lahir   = data.get('tanggal_lahir', '').strip()

    if not all([salutation, first_name, last_name, kewarganegaraan,
                country_code, mobile_number, tanggal_lahir]):
        return False, 'Semua field wajib diisi.'

    if salutation not in SALUTATIONS:
        return False, 'Salutation tidak valid.'

    if not re.match(r"^[A-Za-z\s]+$", first_name):
        return False, 'Nama depan hanya boleh huruf.'

    if middle_name and not re.match(r"^[A-Za-z\s]+$", middle_name):
        return False, 'Nama tengah hanya boleh huruf.'

    if last_name and not re.match(r"^[A-Za-z\s]+$", last_name):
        return False, 'Nama belakang hanya boleh huruf.'

    first_mid = f"{first_name} {middle_name}".strip() if middle_name else first_name
    for value, max_length, label in (
        (first_mid, 100, 'Nama depan/tengah'),
        (last_name, 100, 'Nama belakang'),
        (kewarganegaraan, 50, 'Kewarganegaraan'),
    ):
        err = _validate_max_length(value, max_length, label)
        if err:
            return False, err

    if not re.match(r"^\+\d{1,4}$", country_code):
        return False, 'Kode negara harus format +62.'

    if not mobile_number.isdigit():
        return False, 'Nomor HP hanya boleh angka.'

    if len(mobile_number) < 8 or len(mobile_number) > 15:
        return False, 'Nomor HP harus 8–15 digit.'

    tgl, err = _parse_date(tanggal_lahir, 'tanggal lahir')
    if err:
        return False, err
    today = date.today()
    if tgl > today:
        return False, 'Tanggal lahir tidak boleh di masa depan.'
    umur = (today - tgl).days // 365
    if umur < 10:
        return False, 'Umur minimal 10 tahun.'
    if umur > 120:
        return False, 'Umur tidak valid.'

    return True, {
        'salutation':      salutation,
        'first_mid':       first_mid,
        'last_name':       last_name,
        'kewarganegaraan': kewarganegaraan,
        'country_code':    country_code,
        'mobile_number':   mobile_number,
        'tanggal_lahir':   tgl,
    }


def validate_password_change(password_lama, password_baru, konfirmasi, db_hash):
    if hash_password(password_lama) != db_hash:
        return False, 'Password lama tidak sesuai.'
    if not password_baru:
        return False, 'Password baru tidak boleh kosong.'
    if password_baru != konfirmasi:
        return False, 'Konfirmasi password tidak cocok.'
    if len(password_baru) < 8:
        return False, 'Password minimal 8 karakter.'
    return True, None


def _is_unique_error(e):
    msg = str(e).lower()
    return 'unique' in msg or 'duplicate key' in msg


def _extract_raise_message(e):
    """Extract clean message from PostgreSQL RAISE EXCEPTION."""
    msg = str(e)
    if 'ERROR:' in msg:
        body = msg.split('ERROR:', 1)[1].strip()
        if body.startswith('ERROR:'):
            body = body.split('ERROR:', 1)[1].strip()
        body = body.splitlines()[0].strip()
        return f'ERROR: {body}'
    return msg.splitlines()[0].strip()


# ─── LANDING ──────────────────────────────────────────────────────────────────

def landing(request):
    if request.session.get('role'):
        return redirect('dashboard')
    return render(request, 'landing.html', {'role': 'guest'})


# ─── AUTH: LOGIN & LOGOUT ─────────────────────────────────────────────────────

def login_page(request):
    if request.method == 'POST':
        email    = normalize_email(request.POST.get('email', ''))
        password = request.POST.get('password', '').strip()

        with connection.cursor() as cur:
            cur.execute(
                "SELECT email, salutation, first_mid_name, last_name, role, success, message "
                "FROM verify_login(%s, %s)",
                [email, hash_password(password)]
            )
            row = cur.fetchone()

            if not row or not row[5]:
                return render(request, 'login.html', {
                    'error': row[6] if row else 'Email atau password salah, silakan coba lagi.',
                    'role':  'guest',
                })

            db_email = row[0]
            db_role = row[4]

        request.session['email'] = db_email
        if db_role in ('member', 'staf'):
            request.session['role'] = db_role
        else:
            return render(request, 'login.html', {
                'error': 'Akun tidak memiliki role valid.',
                'role':  'guest',
            })

        return redirect('dashboard')

    return render(request, 'login.html', {'role': 'guest'})


def logout_view(request):
    request.session.flush()
    return redirect('login')


# ─── AUTH: REGISTER ───────────────────────────────────────────────────────────

def register(request):
    if request.method == 'POST':
        role            = request.POST.get('role', '').strip()
        email           = normalize_email(request.POST.get('email', ''))
        password        = request.POST.get('password', '').strip()
        konfirmasi      = request.POST.get('konfirmasi_password', '').strip()
        kode_maskapai   = request.POST.get('kode_maskapai', '').strip()

        if not email or not password:
            request.session['error_msg'] = 'Semua field wajib diisi.'
            return redirect('register')

        err = _validate_max_length(email, 100, 'Email')
        if err:
            request.session['error_msg'] = err
            return redirect('register')

        if role not in ('member', 'staf'):
            request.session['error_msg'] = 'Role tidak valid.'
            return redirect('register')

        if role == 'staf' and not kode_maskapai:
            request.session['error_msg'] = 'Kode maskapai wajib diisi untuk staf.'
            return redirect('register')

        if password != konfirmasi:
            request.session['error_msg'] = 'Konfirmasi password tidak cocok.'
            return redirect('register')

        if len(password) < 8:
            request.session['error_msg'] = 'Password minimal 8 karakter.'
            return redirect('register')

        valid, result = validate_profil_data(request.POST)
        if not valid:
            request.session['error_msg'] = result
            return redirect('register')
        data = result

        try:
            with transaction.atomic():
                with connection.cursor() as cur:
                    cur.execute(
                        "SELECT 1 FROM pengguna WHERE mobile_number = %s", [data['mobile_number']]
                    )
                    if cur.fetchone():
                        request.session['error_msg'] = 'Nomor HP sudah digunakan.'
                        return redirect('register')

                    if role == 'staf' and not _row_exists(cur, 'maskapai', 'kode_maskapai', kode_maskapai):
                        request.session['error_msg'] = 'Kode maskapai tidak valid.'
                        return redirect('register')

                    cur.execute("""
                        INSERT INTO pengguna (
                            email, password, salutation, first_mid_name, last_name,
                            country_code, mobile_number, tanggal_lahir, kewarganegaraan
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, [
                        email, hash_password(password), data['salutation'],
                        data['first_mid'], data['last_name'], data['country_code'],
                        data['mobile_number'], data['tanggal_lahir'],
                        data['kewarganegaraan'],
                    ])

                    if role == 'member':
                        cur.execute(
                            "SELECT id_tier FROM tier ORDER BY minimal_tier_miles ASC LIMIT 1"
                        )
                        tier_id = cur.fetchone()[0]

                        cur.execute("""
                            INSERT INTO member (email, tanggal_bergabung, id_tier,
                                                award_miles, total_miles)
                            VALUES (%s, %s, %s, 0, 0)
                            RETURNING nomor_member
                        """, [email, date.today(), tier_id])
                        nomor_member = cur.fetchone()[0]

                    elif role == 'staf':
                        cur.execute("""
                            INSERT INTO staf (email, kode_maskapai)
                            VALUES (%s, %s)
                            RETURNING id_staf
                        """, [email, kode_maskapai])
                        id_staf = cur.fetchone()[0]

        except Exception as e:
            if _is_unique_error(e):
                extracted = _extract_raise_message(e)
                request.session['error_msg'] = (
                    extracted if extracted.startswith('ERROR:')
                    else 'Data sudah digunakan (email/nomor HP/ID duplikat).'
                )
            else:
                request.session['error_msg'] = _extract_raise_message(e)
            return redirect('register')

        request.session['success_msg'] = 'Registrasi berhasil. Silakan login.'
        return redirect('login')

    # GET — daftar maskapai untuk dropdown staf
    with connection.cursor() as cur:
        cur.execute("SELECT kode_maskapai, nama_maskapai FROM maskapai ORDER BY nama_maskapai")
        maskapai_list = cur.fetchall()

    return render(request, 'register.html', {
        'role':          'guest',
        'maskapai_list': maskapai_list,
        'success_msg':   request.session.pop('success_msg', None),
        'error_msg':     request.session.pop('error_msg', None),
    })


# ─── DASHBOARD ────────────────────────────────────────────────────────────────

def dashboard(request):
    role = request.session.get('role')
    if not role:
        return redirect('login')

    email = request.session.get('email')

    with connection.cursor() as cur:
        if role == 'member':
            cur.execute("""
                SELECT
                    p.salutation, p.first_mid_name, p.last_name,
                    p.email, p.kewarganegaraan,
                    p.country_code, p.mobile_number, p.tanggal_lahir,
                    m.nomor_member, m.tanggal_bergabung,
                    m.award_miles, m.total_miles,
                    t.nama
                FROM pengguna p
                JOIN member m ON p.email = m.email
                JOIN tier   t ON m.id_tier = t.id_tier
                WHERE p.email = %s
            """, [email])
            row = cur.fetchone()
            if not row:
                return redirect('login')

            cur.execute("""
                SELECT 'Transfer Keluar' AS tipe, jumlah * -1 AS jumlah, timestamp
                FROM transfer WHERE email_member_1 = %s
                UNION ALL
                SELECT 'Transfer Masuk', jumlah, timestamp
                FROM transfer WHERE email_member_2 = %s
                UNION ALL
                SELECT 'Redeem', h.miles * -1, r.timestamp
                FROM redeem r JOIN hadiah h ON r.kode_hadiah = h.kode_hadiah
                WHERE r.email_member = %s
                UNION ALL
                SELECT 'Beli Package', ap.jumlah_award_miles, map.timestamp
                FROM member_award_miles_package map
                JOIN award_miles_package ap ON map.id_award_miles_package = ap.id
                WHERE map.email_member = %s
                UNION ALL
                SELECT 'Klaim Disetujui', 1000, timestamp
                FROM claim_missing_miles
                WHERE email_member = %s AND status_penerimaan = 'Disetujui'
                ORDER BY timestamp DESC
                LIMIT 5
            """, [email, email, email, email, email])
            riwayat = [
                _dashboard_activity(tipe, jumlah, timestamp)
                for tipe, jumlah, timestamp in cur.fetchall()
            ]

            member = {
                'nama_lengkap':      f"{row[0]} {row[1]} {row[2]}",
                'email':             row[3],
                'kewarganegaraan':   row[4],
                'telepon':           f"{row[5]}{row[6]}",
                'tanggal_lahir':     row[7],
                'nomor':             row[8],
                'tanggal_bergabung': row[9],
                'award_miles':       row[10],
                'total_miles':       row[11],
                'tier':              row[12],
            }
            return render(request, 'dashboard.html', {
                'role':    'member',
                'member':  member,
                'riwayat': riwayat,
            })

        elif role == 'staf':
            cur.execute("""
                SELECT s.id_staf, m.nama_maskapai, p.first_mid_name, p.last_name,
                       p.salutation, p.email
                FROM staf s
                JOIN maskapai m ON s.kode_maskapai = m.kode_maskapai
                JOIN pengguna p ON s.email = p.email
                WHERE s.email = %s
            """, [email])
            row = cur.fetchone()
            if not row:
                return redirect('login')

            cur.execute(
                "SELECT COUNT(*) FROM claim_missing_miles WHERE status_penerimaan = 'Menunggu'"
            )
            total_menunggu = cur.fetchone()[0]

            cur.execute("""
                SELECT COUNT(*) FROM claim_missing_miles
                WHERE status_penerimaan = 'Disetujui' AND email_staf = %s
            """, [email])
            disetujui_saya = cur.fetchone()[0]

            cur.execute("""
                SELECT COUNT(*) FROM claim_missing_miles
                WHERE status_penerimaan = 'Ditolak' AND email_staf = %s
            """, [email])
            ditolak_saya = cur.fetchone()[0]

            cur.execute("""
                SELECT email_member, bandara_asal, bandara_tujuan, flight_number, timestamp
                FROM claim_missing_miles
                WHERE status_penerimaan = 'Menunggu'
                ORDER BY timestamp ASC
                LIMIT 1
            """)
            next_claim_row = cur.fetchone()

            staf = {
                'id':      row[0],
                'maskapai': row[1],
                'nama':    f"{row[4]} {row[2]} {row[3]}",
                'email':   row[5],
            }
            next_claim = None
            if next_claim_row:
                next_claim = {
                    'email_member': next_claim_row[0],
                    'rute':         f"{next_claim_row[1]} → {next_claim_row[2]}",
                    'flight':       next_claim_row[3],
                    'timestamp':    next_claim_row[4],
                }

            return render(request, 'dashboard_staf.html', {
                'role':           'staf',
                'staf':           staf,
                'total_menunggu': total_menunggu,
                'disetujui_saya': disetujui_saya,
                'ditolak_saya':   ditolak_saya,
                'next_claim':      next_claim,
            })

    return redirect('login')


# ─── PROFIL ───────────────────────────────────────────────────────────────────

def profil(request):
    role = request.session.get('role')
    if not role:
        return redirect('login')

    email = request.session.get('email')

    with connection.cursor() as cur:
        cur.execute("""
            SELECT salutation, first_mid_name, last_name, email,
                   country_code, mobile_number, kewarganegaraan, tanggal_lahir
            FROM pengguna WHERE email = %s
        """, [email])
        p = cur.fetchone()
        if not p:
            return redirect('login')

        user = {
            'salutation': p[0], 'first_mid_name': p[1], 'last_name': p[2],
            'email': p[3], 'country_code': p[4], 'mobile_number': p[5],
            'kewarganegaraan': p[6], 'tanggal_lahir': p[7],
        }

        if role == 'member':
            cur.execute(
                "SELECT nomor_member, tanggal_bergabung FROM member WHERE email = %s", [email]
            )
            m = cur.fetchone()
            member = {'nomor_member': m[0], 'tanggal_bergabung': m[1]} if m else None
            return render(request, 'profil.html', {
                'role': 'member', 'user': user, 'member': member,
                'success_msg': request.session.pop('success_msg', None),
                'error_msg':   request.session.pop('error_msg', None),
            })

        elif role == 'staf':
            cur.execute(
                "SELECT id_staf, kode_maskapai FROM staf WHERE email = %s", [email]
            )
            s = cur.fetchone()
            staf = {'id_staf': s[0], 'kode_maskapai': s[1]} if s else None

            cur.execute(
                "SELECT kode_maskapai, nama_maskapai FROM maskapai ORDER BY nama_maskapai"
            )
            maskapai_list = cur.fetchall()

            return render(request, 'profil.html', {
                'role': 'staf', 'user': user, 'staf': staf,
                'maskapai_list': maskapai_list,
                'success_msg': request.session.pop('success_msg', None),
                'error_msg':   request.session.pop('error_msg', None),
            })

    return redirect('login')


def profil_update(request):
    role = request.session.get('role')
    if not role or request.method != 'POST':
        return redirect('profil')

    email = request.session.get('email')
    valid, result = validate_profil_data(request.POST)
    if not valid:
        request.session['error_msg'] = result
        return redirect('profil')

    data = result
    try:
        with transaction.atomic():
            with connection.cursor() as cur:
                cur.execute("""
                    UPDATE pengguna SET
                        salutation      = %s,
                        first_mid_name  = %s,
                        last_name       = %s,
                        kewarganegaraan = %s,
                        country_code    = %s,
                        mobile_number   = %s,
                        tanggal_lahir   = %s
                    WHERE email = %s
                """, [
                    data['salutation'], data['first_mid'], data['last_name'],
                    data['kewarganegaraan'], data['country_code'],
                    data['mobile_number'], data['tanggal_lahir'], email,
                ])

                if role == 'staf':
                    kode_maskapai = request.POST.get('kode_maskapai', '').strip()
                    if kode_maskapai:
                        if not _row_exists(cur, 'maskapai', 'kode_maskapai', kode_maskapai):
                            request.session['error_msg'] = 'Kode maskapai tidak valid.'
                            return redirect('profil')
                        cur.execute(
                            "UPDATE staf SET kode_maskapai = %s WHERE email = %s",
                            [kode_maskapai, email]
                        )

        request.session['success_msg'] = 'Perubahan berhasil disimpan.'
    except Exception as e:
        request.session['error_msg'] = f'Gagal menyimpan: {_extract_raise_message(e)}'

    return redirect('profil')


def profil_ubah_password(request):
    role = request.session.get('role')
    if not role or request.method != 'POST':
        return redirect('profil')

    email         = request.session.get('email')
    password_lama = request.POST.get('password_lama', '')
    password_baru = request.POST.get('password_baru', '')
    konfirmasi    = request.POST.get('konfirmasi_password', '')

    with connection.cursor() as cur:
        cur.execute("SELECT password FROM pengguna WHERE email = %s", [email])
        row = cur.fetchone()

    if not row:
        request.session['error_msg'] = 'User tidak ditemukan.'
        return redirect('profil')

    valid, msg = validate_password_change(password_lama, password_baru, konfirmasi, row[0])
    if not valid:
        request.session['error_msg'] = msg
        return redirect('profil')

    try:
        with transaction.atomic():
            with connection.cursor() as cur:
                cur.execute(
                    "UPDATE pengguna SET password = %s WHERE email = %s",
                    [hash_password(password_baru), email]
                )
        request.session['success_msg'] = 'Password berhasil diubah.'
    except Exception as e:
        request.session['error_msg'] = f'Gagal: {_extract_raise_message(e)}'

    return redirect('profil')


# ─── TIER ─────────────────────────────────────────────────────────────────────

def tier(request):
    role = request.session.get('role')
    if not role:
        return redirect('login')
    if role == 'staf':
        return redirect('dashboard')

    email = request.session.get('email')

    with connection.cursor() as cur:
        cur.execute("""
            SELECT m.total_miles, m.award_miles, t.id_tier, t.nama,
                   t.minimal_tier_miles, t.minimal_frekuensi_terbang
            FROM member m JOIN tier t ON m.id_tier = t.id_tier
            WHERE m.email = %s
        """, [email])
        row = cur.fetchone()
        if not row:
            return redirect('login')

        total_miles        = row[0]
        award_miles        = row[1]
        id_tier_saat_ini   = row[2]
        nama_tier_saat_ini = row[3]

        cur.execute("""
            SELECT id_tier, nama, minimal_tier_miles, minimal_frekuensi_terbang
            FROM tier ORDER BY minimal_tier_miles ASC
        """)
        semua_tier_raw = cur.fetchall()

        cur.execute("""
            SELECT COUNT(*) FROM claim_missing_miles
            WHERE email_member = %s AND status_penerimaan = 'Disetujui'
        """, [email])
        frekuensi = cur.fetchone()[0]

    semua_tier = []
    tier_saat_ini_data = None
    tier_berikutnya    = None

    for i, t_row in enumerate(semua_tier_raw):
        tid, tnama, tmin_miles, tmin_frek = t_row
        is_current = (tid == id_tier_saat_ini)
        tier_data = {
            'id_tier':                   tid,
            'nama':                      tnama,
            'minimal_tier_miles':        tmin_miles,
            'minimal_frekuensi_terbang': tmin_frek,
            'is_current':                is_current,
        }
        semua_tier.append(tier_data)
        if is_current:
            tier_saat_ini_data = tier_data
            if i + 1 < len(semua_tier_raw):
                nxt = semua_tier_raw[i + 1]
                tier_berikutnya = {
                    'nama':                      nxt[1],
                    'minimal_tier_miles':        nxt[2],
                    'minimal_frekuensi_terbang': nxt[3],
                }

    miles_needed = (tier_berikutnya['minimal_tier_miles'] - total_miles) if tier_berikutnya else 0
    max_miles    = tier_berikutnya['minimal_tier_miles'] if tier_berikutnya else (tier_saat_ini_data['minimal_tier_miles'] or 1)
    progress_pct = round(min(total_miles / max_miles * 100, 100), 2) if max_miles else 100

    context = {
        'role':            'member',
        'email':           email,
        'tier_saat_ini':   tier_saat_ini_data,
        'tier_berikutnya': tier_berikutnya,
        'progress': {
            'total_miles':         total_miles,
            'award_miles':         award_miles,
            'total_penerbangan':   frekuensi,
            'miles_needed':        max(0, miles_needed),
            'progress_percentage': progress_pct,
        },
        'semua_tier': semua_tier,
    }
    return render(request, 'tier.html', context)


# ─── IDENTITAS ────────────────────────────────────────────────────────────────

def identitas(request):
    role = request.session.get('role')
    if not role or role != 'member':
        return redirect('login')

    email = request.session.get('email')
    today = date.today()

    with connection.cursor() as cur:
        cur.execute("""
            SELECT nomor, jenis, negara_penerbit, tanggal_terbit, tanggal_habis
            FROM identitas WHERE email_member = %s
            ORDER BY tanggal_habis DESC
        """, [email])
        rows = cur.fetchall()
        identity_types = _fetch_identity_types(cur)

    identitas_list = []
    for r in rows:
        identitas_list.append({
            'nomor':           r[0],
            'jenis':           r[1],
            'negara_penerbit': r[2],
            'tanggal_terbit':  r[3],
            'tanggal_habis':   r[4],
            'expired':         r[4] < today if r[4] else False,
        })

    return render(request, 'identitas.html', {
        'role':           'member',
        'identitas_list': identitas_list,
        'identity_types': identity_types,
        'success_msg':    request.session.pop('success_msg', None),
        'error_msg':      request.session.pop('error_msg', None),
    })


def identitas_tambah(request):
    role = request.session.get('role')
    if not role or role != 'member' or request.method != 'POST':
        return redirect('identitas')

    email           = request.session.get('email')
    nomor           = request.POST.get('nomor', '').strip()
    jenis           = request.POST.get('jenis', '').strip()
    negara_penerbit = request.POST.get('negara_penerbit', '').strip()
    tanggal_terbit  = request.POST.get('tanggal_terbit', '').strip()
    tanggal_habis   = request.POST.get('tanggal_habis', '').strip()

    if not all([nomor, jenis, negara_penerbit, tanggal_terbit, tanggal_habis]):
        request.session['error_msg'] = 'Semua field wajib diisi.'
        return redirect('identitas')

    if not _identity_type_exists(jenis):
        request.session['error_msg'] = 'Jenis identitas tidak valid.'
        return redirect('identitas')

    for value, max_length, label in (
        (nomor, 50, 'Nomor dokumen'),
        (negara_penerbit, 50, 'Negara penerbit'),
    ):
        err = _validate_max_length(value, max_length, label)
        if err:
            request.session['error_msg'] = err
            return redirect('identitas')

    tanggal_terbit_date, tanggal_habis_date, err = _validate_identity_dates(tanggal_terbit, tanggal_habis)
    if err:
        request.session['error_msg'] = err
        return redirect('identitas')

    try:
        with transaction.atomic():
            with connection.cursor() as cur:
                cur.execute("""
                    INSERT INTO identitas (nomor, email_member, tanggal_habis, tanggal_terbit,
                                          negara_penerbit, jenis)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, [nomor, email, tanggal_habis_date, tanggal_terbit_date, negara_penerbit, jenis])
        request.session['success_msg'] = 'Identitas berhasil ditambahkan.'
    except Exception as e:
        if _is_unique_error(e):
            request.session['error_msg'] = f'Nomor dokumen {nomor} sudah terdaftar.'
        else:
            request.session['error_msg'] = f'Gagal: {_extract_raise_message(e)}'

    return redirect('identitas')


def identitas_edit(request, nomor):
    role = request.session.get('role')
    if not role or role != 'member' or request.method != 'POST':
        return redirect('identitas')

    email           = request.session.get('email')
    negara_penerbit = request.POST.get('negara_penerbit', '').strip()
    tanggal_terbit  = request.POST.get('tanggal_terbit', '').strip()
    tanggal_habis   = request.POST.get('tanggal_habis', '').strip()

    if not all([negara_penerbit, tanggal_terbit, tanggal_habis]):
        request.session['error_msg'] = 'Semua field wajib diisi.'
        return redirect('identitas')

    err = _validate_max_length(negara_penerbit, 50, 'Negara penerbit')
    if err:
        request.session['error_msg'] = err
        return redirect('identitas')

    tanggal_terbit_date, tanggal_habis_date, err = _validate_identity_dates(tanggal_terbit, tanggal_habis)
    if err:
        request.session['error_msg'] = err
        return redirect('identitas')

    try:
        with transaction.atomic():
            with connection.cursor() as cur:
                cur.execute("""
                    UPDATE identitas
                    SET negara_penerbit = %s, tanggal_terbit = %s, tanggal_habis = %s
                    WHERE nomor = %s AND email_member = %s
                """, [negara_penerbit, tanggal_terbit_date, tanggal_habis_date, nomor, email])
        request.session['success_msg'] = 'Identitas berhasil diperbarui.'
    except Exception as e:
        request.session['error_msg'] = f'Gagal: {_extract_raise_message(e)}'

    return redirect('identitas')


def identitas_hapus(request, nomor):
    role = request.session.get('role')
    if not role or role != 'member' or request.method != 'POST':
        return redirect('identitas')

    email = request.session.get('email')
    try:
        with transaction.atomic():
            with connection.cursor() as cur:
                cur.execute(
                    "DELETE FROM identitas WHERE nomor = %s AND email_member = %s",
                    [nomor, email]
                )
        request.session['success_msg'] = 'Identitas berhasil dihapus.'
    except Exception as e:
        request.session['error_msg'] = f'Gagal: {_extract_raise_message(e)}'

    return redirect('identitas')


# ─── KLAIM MISSING MILES — MEMBER (CRUD) ─────────────────────────────────────

def _get_ref_data(cur):
    cur.execute("SELECT iata_code, nama FROM bandara ORDER BY iata_code")
    bandara_list = cur.fetchall()
    cur.execute("SELECT kode_maskapai, nama_maskapai FROM maskapai ORDER BY nama_maskapai")
    maskapai_list = cur.fetchall()
    return bandara_list, maskapai_list


def klaim_member(request):
    role = request.session.get('role')
    if not role or role != 'member':
        return redirect('login')

    email         = request.session.get('email')
    status_filter = request.GET.get('status', 'semua')
    if status_filter != 'semua' and status_filter not in CLAIM_STATUSES:
        status_filter = 'semua'

    with connection.cursor() as cur:
        query = """
            SELECT c.id, c.maskapai, mk.nama_maskapai,
                   c.bandara_asal, ba.nama, c.bandara_tujuan, bt.nama,
                   c.tanggal_penerbangan, c.flight_number, c.nomor_tiket,
                   c.kelas_kabin, c.pnr, c.status_penerimaan, c.timestamp
            FROM claim_missing_miles c
            JOIN maskapai mk ON c.maskapai = mk.kode_maskapai
            JOIN bandara ba  ON c.bandara_asal    = ba.iata_code
            JOIN bandara bt  ON c.bandara_tujuan  = bt.iata_code
            WHERE c.email_member = %s
        """
        params = [email]
        if status_filter != 'semua':
            query += " AND c.status_penerimaan = %s"
            params.append(status_filter)
        query += " ORDER BY c.timestamp DESC"

        cur.execute(query, params)
        rows = cur.fetchall()
        klaim_list = []
        for r in rows:
            klaim_list.append({
                'id': r[0], 'maskapai': r[1], 'nama_maskapai': r[2],
                'bandara_asal': r[3], 'nama_asal': r[4],
                'bandara_tujuan': r[5], 'nama_tujuan': r[6],
                'rute': f"{r[3]} → {r[5]}",
                'tanggal_penerbangan': r[7], 'flight_number': r[8],
                'nomor_tiket': r[9], 'kelas_kabin': r[10], 'pnr': r[11],
                'status_penerimaan': r[12], 'timestamp': r[13],
            })

        cur.execute("""
            SELECT status_penerimaan, COUNT(*) FROM claim_missing_miles
            WHERE email_member = %s GROUP BY status_penerimaan
        """, [email])
        stat_rows = cur.fetchall()
        stats = {'total': 0, 'menunggu': 0, 'disetujui': 0, 'ditolak': 0}
        for s, c in stat_rows:
            stats['total'] += c
            if s == 'Menunggu':    stats['menunggu']  = c
            elif s == 'Disetujui': stats['disetujui'] = c
            elif s == 'Ditolak':   stats['ditolak']   = c

        bandara_list, maskapai_list = _get_ref_data(cur)

    return render(request, 'klaim_member.html', {
        'role': 'member', 'klaim_list': klaim_list,
        'status_filter': status_filter, 'stats': stats,
        'bandara_list': bandara_list, 'maskapai_list': maskapai_list,
        'kelas_list': ['Economy', 'Business', 'First'],
        'success_msg': request.session.pop('success_msg', None),
        'error_msg':   request.session.pop('error_msg', None),
    })


def klaim_ajukan(request):
    role = request.session.get('role')
    if not role or role != 'member' or request.method != 'POST':
        return redirect('klaim_member')

    email           = request.session.get('email')
    maskapai        = request.POST.get('maskapai', '').strip()
    bandara_asal    = request.POST.get('bandara_asal', '').strip()
    bandara_tujuan  = request.POST.get('bandara_tujuan', '').strip()
    tgl_penerbangan = request.POST.get('tanggal_penerbangan', '').strip()
    flight_number   = request.POST.get('flight_number', '').strip()
    nomor_tiket     = request.POST.get('nomor_tiket', '').strip()
    kelas_kabin     = request.POST.get('kelas_kabin', '').strip()
    pnr             = request.POST.get('pnr', '').strip()

    if not all([maskapai, bandara_asal, bandara_tujuan,
                tgl_penerbangan, flight_number, nomor_tiket, kelas_kabin, pnr]):
        request.session['error_msg'] = 'Semua field wajib diisi.'
        return redirect('klaim_member')

    if bandara_asal == bandara_tujuan:
        request.session['error_msg'] = 'Bandara asal dan tujuan tidak boleh sama.'
        return redirect('klaim_member')

    if kelas_kabin not in CABIN_CLASSES:
        request.session['error_msg'] = 'Kelas kabin tidak valid.'
        return redirect('klaim_member')

    tgl_penerbangan_date, err = _parse_date(tgl_penerbangan, 'tanggal penerbangan')
    if err:
        request.session['error_msg'] = err
        return redirect('klaim_member')
    if tgl_penerbangan_date > date.today():
        request.session['error_msg'] = 'Tanggal penerbangan tidak boleh di masa depan.'
        return redirect('klaim_member')

    for value, max_length, label in (
        (flight_number, 10, 'Flight number'),
        (nomor_tiket, 20, 'Nomor tiket'),
        (pnr, 10, 'PNR'),
    ):
        err = _validate_max_length(value, max_length, label)
        if err:
            request.session['error_msg'] = err
            return redirect('klaim_member')

    try:
        with transaction.atomic():
            with connection.cursor() as cur:
                if not _row_exists(cur, 'maskapai', 'kode_maskapai', maskapai):
                    request.session['error_msg'] = 'Maskapai tidak valid.'
                    return redirect('klaim_member')
                if not _row_exists(cur, 'bandara', 'iata_code', bandara_asal):
                    request.session['error_msg'] = 'Bandara asal tidak valid.'
                    return redirect('klaim_member')
                if not _row_exists(cur, 'bandara', 'iata_code', bandara_tujuan):
                    request.session['error_msg'] = 'Bandara tujuan tidak valid.'
                    return redirect('klaim_member')

                cur.execute("""
                    INSERT INTO claim_missing_miles
                        (email_member, maskapai, bandara_asal, bandara_tujuan,
                         tanggal_penerbangan, flight_number, nomor_tiket,
                         kelas_kabin, pnr, status_penerimaan, timestamp)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,'Menunggu', NOW())
                """, [email, maskapai, bandara_asal, bandara_tujuan,
                      tgl_penerbangan_date, flight_number, nomor_tiket, kelas_kabin, pnr])
        request.session['success_msg'] = 'Klaim berhasil diajukan!'
    except Exception as e:
        if _is_unique_error(e):
            request.session['error_msg'] = (
                f'ERROR: Klaim untuk penerbangan "{flight_number}" pada tanggal '
                f'"{tgl_penerbangan}" dengan nomor tiket "{nomor_tiket}" sudah pernah diajukan sebelumnya.'
            )
        else:
            request.session['error_msg'] = _extract_raise_message(e)

    return redirect('klaim_member')


def klaim_edit(request, klaim_id):
    role = request.session.get('role')
    if not role or role != 'member' or request.method != 'POST':
        return redirect('klaim_member')

    email           = request.session.get('email')
    maskapai        = request.POST.get('maskapai', '').strip()
    bandara_asal    = request.POST.get('bandara_asal', '').strip()
    bandara_tujuan  = request.POST.get('bandara_tujuan', '').strip()
    tgl_penerbangan = request.POST.get('tanggal_penerbangan', '').strip()
    flight_number   = request.POST.get('flight_number', '').strip()
    nomor_tiket     = request.POST.get('nomor_tiket', '').strip()
    kelas_kabin     = request.POST.get('kelas_kabin', '').strip()
    pnr             = request.POST.get('pnr', '').strip()

    if not all([maskapai, bandara_asal, bandara_tujuan,
                tgl_penerbangan, flight_number, nomor_tiket, kelas_kabin, pnr]):
        request.session['error_msg'] = 'Semua field wajib diisi.'
        return redirect('klaim_member')

    if bandara_asal == bandara_tujuan:
        request.session['error_msg'] = 'Bandara asal dan tujuan tidak boleh sama.'
        return redirect('klaim_member')

    if kelas_kabin not in CABIN_CLASSES:
        request.session['error_msg'] = 'Kelas kabin tidak valid.'
        return redirect('klaim_member')

    tgl_penerbangan_date, err = _parse_date(tgl_penerbangan, 'tanggal penerbangan')
    if err:
        request.session['error_msg'] = err
        return redirect('klaim_member')
    if tgl_penerbangan_date > date.today():
        request.session['error_msg'] = 'Tanggal penerbangan tidak boleh di masa depan.'
        return redirect('klaim_member')

    for value, max_length, label in (
        (flight_number, 10, 'Flight number'),
        (nomor_tiket, 20, 'Nomor tiket'),
        (pnr, 10, 'PNR'),
    ):
        err = _validate_max_length(value, max_length, label)
        if err:
            request.session['error_msg'] = err
            return redirect('klaim_member')

    with connection.cursor() as cur:
        cur.execute("""
            SELECT status_penerimaan FROM claim_missing_miles
            WHERE id = %s AND email_member = %s
        """, [klaim_id, email])
        row = cur.fetchone()

    if not row:
        request.session['error_msg'] = 'Klaim tidak ditemukan.'
        return redirect('klaim_member')
    if row[0] != 'Menunggu':
        request.session['error_msg'] = 'Hanya klaim berstatus Menunggu yang dapat diedit.'
        return redirect('klaim_member')

    try:
        with transaction.atomic():
            with connection.cursor() as cur:
                if not _row_exists(cur, 'maskapai', 'kode_maskapai', maskapai):
                    request.session['error_msg'] = 'Maskapai tidak valid.'
                    return redirect('klaim_member')
                if not _row_exists(cur, 'bandara', 'iata_code', bandara_asal):
                    request.session['error_msg'] = 'Bandara asal tidak valid.'
                    return redirect('klaim_member')
                if not _row_exists(cur, 'bandara', 'iata_code', bandara_tujuan):
                    request.session['error_msg'] = 'Bandara tujuan tidak valid.'
                    return redirect('klaim_member')

                cur.execute("""
                    UPDATE claim_missing_miles SET
                        maskapai = %s, bandara_asal = %s, bandara_tujuan = %s,
                        tanggal_penerbangan = %s, flight_number = %s,
                        nomor_tiket = %s, kelas_kabin = %s, pnr = %s
                    WHERE id = %s AND email_member = %s AND status_penerimaan = 'Menunggu'
                """, [maskapai, bandara_asal, bandara_tujuan, tgl_penerbangan_date,
                      flight_number, nomor_tiket, kelas_kabin, pnr, klaim_id, email])
        request.session['success_msg'] = 'Klaim berhasil diperbarui.'
    except Exception as e:
        if _is_unique_error(e):
            request.session['error_msg'] = 'Klaim duplikat terdeteksi.'
        else:
            request.session['error_msg'] = f'Gagal: {_extract_raise_message(e)}'

    return redirect('klaim_member')


def klaim_batalkan(request, klaim_id):
    role = request.session.get('role')
    if not role or role != 'member' or request.method != 'POST':
        return redirect('klaim_member')

    email = request.session.get('email')

    with connection.cursor() as cur:
        cur.execute("""
            SELECT status_penerimaan FROM claim_missing_miles
            WHERE id = %s AND email_member = %s
        """, [klaim_id, email])
        row = cur.fetchone()

    if not row:
        request.session['error_msg'] = 'Klaim tidak ditemukan.'
        return redirect('klaim_member')
    if row[0] != 'Menunggu':
        request.session['error_msg'] = 'Hanya klaim berstatus Menunggu yang dapat dibatalkan.'
        return redirect('klaim_member')

    try:
        with transaction.atomic():
            with connection.cursor() as cur:
                cur.execute(
                    "DELETE FROM claim_missing_miles WHERE id = %s AND email_member = %s AND status_penerimaan = 'Menunggu'",
                    [klaim_id, email]
                )
        request.session['success_msg'] = 'Klaim berhasil dibatalkan.'
    except Exception as e:
        request.session['error_msg'] = f'Gagal: {_extract_raise_message(e)}'

    return redirect('klaim_member')


# ─── KLAIM MISSING MILES — STAF (RU) ─────────────────────────────────────────

def klaim_staf(request):
    role = request.session.get('role')
    if not role or role != 'staf':
        return redirect('login')

    email_staf      = request.session.get('email')
    status_filter   = request.GET.get('status', 'semua')
    maskapai_filter = request.GET.get('maskapai', 'semua')
    tgl_dari        = request.GET.get('tgl_dari', '')
    tgl_sampai      = request.GET.get('tgl_sampai', '')
    search          = request.GET.get('search', '').strip()

    if status_filter != 'semua' and status_filter not in CLAIM_STATUSES:
        status_filter = 'semua'
    if tgl_dari and _parse_date(tgl_dari, 'tanggal dari')[1]:
        tgl_dari = ''
    if tgl_sampai and _parse_date(tgl_sampai, 'tanggal sampai')[1]:
        tgl_sampai = ''

    with connection.cursor() as cur:
        params = []
        conditions = ["1=1"]

        if status_filter != 'semua':
            conditions.append("c.status_penerimaan = %s")
            params.append(status_filter)
        if maskapai_filter != 'semua':
            conditions.append("c.maskapai = %s")
            params.append(maskapai_filter)
        if tgl_dari:
            conditions.append("c.timestamp::date >= %s")
            params.append(tgl_dari)
        if tgl_sampai:
            conditions.append("c.timestamp::date <= %s")
            params.append(tgl_sampai)
        if search:
            conditions.append(
                "(LOWER(c.email_member) LIKE %s OR LOWER(p.first_mid_name) LIKE %s)"
            )
            params += [f'%{search.lower()}%', f'%{search.lower()}%']

        where_clause = " AND ".join(conditions)
        cur.execute(f"""
            SELECT c.id, p.first_mid_name || ' ' || p.last_name AS nama_member,
                   c.email_member, mk.nama_maskapai,
                   c.bandara_asal, c.bandara_tujuan,
                   c.tanggal_penerbangan, c.flight_number, c.kelas_kabin,
                   c.status_penerimaan, c.timestamp, c.email_staf
            FROM claim_missing_miles c
            JOIN maskapai mk ON c.maskapai = mk.kode_maskapai
            JOIN pengguna p  ON c.email_member = p.email
            WHERE {where_clause}
            ORDER BY c.timestamp DESC
        """, params)
        rows = cur.fetchall()
        klaim_list = []
        for r in rows:
            klaim_list.append({
                'id': r[0],
                'nomor_klaim': f"KLM-{r[0]:04d}",
                'nama_member': r[1], 'email_member': r[2],
                'nama_maskapai': r[3],
                'bandara_asal': r[4], 'bandara_tujuan': r[5],
                'rute': f"{r[4]} → {r[5]}",
                'tanggal_penerbangan': r[6], 'flight_number': r[7],
                'kelas_kabin': r[8], 'status_penerimaan': r[9],
                'timestamp': r[10], 'email_staf': r[11],
            })

        cur.execute("SELECT COUNT(*) FROM claim_missing_miles WHERE status_penerimaan = 'Menunggu'")
        total_menunggu = cur.fetchone()[0]
        cur.execute("""
            SELECT COUNT(*) FROM claim_missing_miles
            WHERE status_penerimaan = 'Disetujui' AND email_staf = %s
        """, [email_staf])
        disetujui_saya = cur.fetchone()[0]
        cur.execute("""
            SELECT COUNT(*) FROM claim_missing_miles
            WHERE status_penerimaan = 'Ditolak' AND email_staf = %s
        """, [email_staf])
        ditolak_saya = cur.fetchone()[0]

        cur.execute("SELECT kode_maskapai, nama_maskapai FROM maskapai ORDER BY nama_maskapai")
        maskapai_list = cur.fetchall()

        cur.execute("""
            SELECT c.id, p.first_mid_name || ' ' || p.last_name AS nama_member,
                   c.email_member, c.bandara_asal, c.bandara_tujuan,
                   c.flight_number, c.timestamp
            FROM claim_missing_miles c
            JOIN pengguna p ON c.email_member = p.email
            WHERE c.status_penerimaan = 'Menunggu'
            ORDER BY c.timestamp ASC
            LIMIT 1
        """)
        next_claim_row = cur.fetchone()

    return render(request, 'klaim_staf.html', {
        'role': 'staf', 'klaim_list': klaim_list,
        'maskapai_list': maskapai_list,
        'stats': {
            'total_menunggu': total_menunggu,
            'disetujui_saya': disetujui_saya,
            'ditolak_saya':   ditolak_saya,
            'total_ditampilkan': len(klaim_list),
        },
        'next_claim': {
            'nomor_klaim': f"KLM-{next_claim_row[0]:04d}",
            'nama_member': next_claim_row[1],
            'email_member': next_claim_row[2],
            'rute': f"{next_claim_row[3]} → {next_claim_row[4]}",
            'flight_number': next_claim_row[5],
            'timestamp': next_claim_row[6],
        } if next_claim_row else None,
        'status_filter': status_filter, 'maskapai_filter': maskapai_filter,
        'tgl_dari': tgl_dari, 'tgl_sampai': tgl_sampai, 'search': search,
        'success_msg': request.session.pop('success_msg', None),
        'error_msg':   request.session.pop('error_msg', None),
    })


def klaim_proses(request, klaim_id):
    role = request.session.get('role')
    if not role or role != 'staf' or request.method != 'POST':
        return redirect('klaim_staf')

    email_staf = request.session.get('email')
    aksi       = request.POST.get('aksi', '')

    if aksi not in ('setujui', 'tolak'):
        request.session['error_msg'] = 'Aksi tidak valid.'
        return redirect('klaim_staf')

    with connection.cursor() as cur:
        cur.execute(
            "SELECT status_penerimaan FROM claim_missing_miles WHERE id = %s", [klaim_id]
        )
        row = cur.fetchone()

    if not row:
        request.session['error_msg'] = 'Klaim tidak ditemukan.'
        return redirect('klaim_staf')
    if row[0] != 'Menunggu':
        request.session['error_msg'] = 'Klaim ini sudah diproses sebelumnya.'
        return redirect('klaim_staf')

    status_baru = 'Disetujui' if aksi == 'setujui' else 'Ditolak'

    try:
        with transaction.atomic():
            with connection.cursor() as cur:
                cur.execute("""
                    UPDATE claim_missing_miles
                    SET status_penerimaan = %s, email_staf = %s
                    WHERE id = %s AND status_penerimaan = 'Menunggu'
                    RETURNING email_member
                """, [status_baru, email_staf, klaim_id])
                updated = cur.fetchone()
                if not updated:
                    request.session['error_msg'] = 'Klaim ini sudah diproses sebelumnya.'
                    return redirect('klaim_staf')

        if aksi == 'setujui':
            request.session['success_msg'] = 'Klaim DISETUJUI. Miles ditambahkan ke akun member.'
        else:
            request.session['success_msg'] = 'Klaim DITOLAK.'

    except Exception as e:
        request.session['error_msg'] = _extract_raise_message(e)

    return redirect('klaim_staf')


# ─── TRANSFER MILES ───────────────────────────────────────────────────────────

def transfer_miles(request):
    role = request.session.get('role')
    if not role or role != 'member':
        return redirect('login')

    email = request.session.get('email')

    with connection.cursor() as cur:
        cur.execute("SELECT award_miles FROM member WHERE email = %s", [email])
        row = cur.fetchone()
        award_miles = row[0] if row else 0

        cur.execute("""
            SELECT t.email_member_1, p1.first_mid_name || ' ' || p1.last_name,
                   t.email_member_2, p2.first_mid_name || ' ' || p2.last_name,
                   t.jumlah, t.catatan, t.timestamp
            FROM transfer t
            JOIN pengguna p1 ON t.email_member_1 = p1.email
            JOIN pengguna p2 ON t.email_member_2 = p2.email
            WHERE t.email_member_1 = %s OR t.email_member_2 = %s
            ORDER BY t.timestamp DESC
        """, [email, email])
        rows = cur.fetchall()

    riwayat      = []
    total_keluar = 0
    total_masuk  = 0
    for r in rows:
        if r[0] == email:
            tipe       = 'keluar'
            total_keluar += r[4]
            email_lain = r[2]
            nama_lain  = r[3]
        else:
            tipe       = 'masuk'
            total_masuk += r[4]
            email_lain = r[0]
            nama_lain  = r[1]
        riwayat.append({
            'email_dari': r[0], 'nama_dari': r[1],
            'email_ke':   r[2], 'nama_ke':   r[3],
            'jumlah': r[4], 'catatan': r[5], 'timestamp': r[6],
            'tipe': tipe, 'email_lain': email_lain, 'nama_lain': nama_lain,
        })

    return render(request, 'transfer.html', {
        'role':        'member',
        'award_miles': award_miles,
        'riwayat':     riwayat,
        'stats': {'total_keluar': total_keluar, 'total_masuk': total_masuk},
        'success_msg': request.session.pop('success_msg', None),
        'error_msg':   request.session.pop('error_msg', None),
    })


def transfer_kirim(request):
    role = request.session.get('role')
    if not role or role != 'member' or request.method != 'POST':
        return redirect('transfer_miles')

    email_dari   = request.session.get('email')
    email_tujuan = normalize_email(request.POST.get('email_tujuan', ''))
    jumlah_str   = request.POST.get('jumlah', '').strip()
    catatan      = request.POST.get('catatan', '').strip() or None

    if not email_tujuan or not jumlah_str:
        request.session['error_msg'] = 'Email tujuan dan jumlah wajib diisi.'
        return redirect('transfer_miles')

    if email_tujuan.lower() == email_dari.lower():
        request.session['error_msg'] = 'Tidak dapat transfer ke diri sendiri.'
        return redirect('transfer_miles')

    jumlah, err = _validate_positive_int(jumlah_str, 'Jumlah miles')
    if err:
        request.session['error_msg'] = err
        return redirect('transfer_miles')

    if catatan:
        err = _validate_max_length(catatan, 255, 'Catatan')
        if err:
            request.session['error_msg'] = err
            return redirect('transfer_miles')

    err = _validate_max_length(email_tujuan, 100, 'Email tujuan')
    if err:
        request.session['error_msg'] = err
        return redirect('transfer_miles')

    try:
        with transaction.atomic():
            with connection.cursor() as cur:
                cur.execute("""
                    INSERT INTO transfer (email_member_1, email_member_2, timestamp, jumlah, catatan)
                    VALUES (%s, %s, NOW(), %s, %s)
                """, [email_dari, email_tujuan, jumlah, catatan])
        request.session['success_msg'] = (
            f'SUKSES: Transfer {jumlah} miles dari "{email_dari}" ke "{email_tujuan}" berhasil dicatat.'
        )
    except Exception as e:
        request.session['error_msg'] = _extract_raise_message(e)

    return redirect('transfer_miles')


# ─── REDEEM HADIAH ────────────────────────────────────────────────────────────

def redeem_hadiah(request):
    role = request.session.get('role')
    if not role or role != 'member':
        return redirect('login')

    email = request.session.get('email')

    with connection.cursor() as cur:
        cur.execute("SELECT award_miles FROM member WHERE email = %s", [email])
        award_miles = cur.fetchone()[0]

        cur.execute("""
            SELECT kode_hadiah, nama, miles, deskripsi, valid_start_date, program_end, id_penyedia
            FROM hadiah
            WHERE program_end >= CURRENT_DATE AND valid_start_date <= CURRENT_DATE
            ORDER BY miles ASC
        """)
        hadiah_list = []
        for r in cur.fetchall():
            hadiah_list.append({
                'kode_hadiah': r[0], 'nama': r[1], 'miles': r[2],
                'deskripsi': r[3], 'valid_start_date': r[4], 'program_end': r[5],
                'id_penyedia': r[6],
            })

        cur.execute("""
            SELECT r.kode_hadiah, h.nama, h.miles, r.timestamp
            FROM redeem r JOIN hadiah h ON r.kode_hadiah = h.kode_hadiah
            WHERE r.email_member = %s
            ORDER BY r.timestamp DESC
        """, [email])
        riwayat_redeem        = []
        total_miles_digunakan = 0
        for r in cur.fetchall():
            riwayat_redeem.append({
                'kode_hadiah': r[0], 'nama_hadiah': r[1], 'miles': r[2], 'timestamp': r[3],
            })
            total_miles_digunakan += r[2]

    return render(request, 'redeem.html', {
        'role':           'member',
        'award_miles':    award_miles,
        'hadiah_list':    hadiah_list,
        'riwayat_redeem': riwayat_redeem,
        'stats': {
            'total_redeem':    len(riwayat_redeem),
            'miles_digunakan': total_miles_digunakan,
        },
        'success_msg': request.session.pop('success_msg', None),
        'error_msg':   request.session.pop('error_msg', None),
    })


def redeem_proses(request):
    role = request.session.get('role')
    if not role or role != 'member' or request.method != 'POST':
        return redirect('redeem_hadiah')

    email       = request.session.get('email')
    kode_hadiah = request.POST.get('kode_hadiah', '').strip()

    if not kode_hadiah:
        request.session['error_msg'] = 'Kode hadiah tidak valid.'
        return redirect('redeem_hadiah')

    with connection.cursor() as cur:
        cur.execute("SELECT nama, miles FROM hadiah WHERE kode_hadiah = %s", [kode_hadiah])
        hadiah = cur.fetchone()

    if not hadiah:
        request.session['error_msg'] = 'Hadiah tidak ditemukan.'
        return redirect('redeem_hadiah')

    nama_hadiah, miles_hadiah = hadiah

    try:
        with transaction.atomic():
            with connection.cursor() as cur:
                cur.execute("""
                    INSERT INTO redeem (email_member, kode_hadiah, timestamp)
                    VALUES (%s, %s, NOW())
                """, [email, kode_hadiah])
        request.session['success_msg'] = (
            f'SUKSES: Redeem hadiah "{nama_hadiah}" berhasil. '
            f'Award miles Anda berkurang {miles_hadiah} miles.'
        )
    except Exception as e:
        request.session['error_msg'] = _extract_raise_message(e)

    return redirect('redeem_hadiah')


# ─── BELI AWARD MILES PACKAGE ─────────────────────────────────────────────────

def beli_package(request):
    role = request.session.get('role')
    if not role or role != 'member':
        return redirect('login')

    email = request.session.get('email')

    with connection.cursor() as cur:
        cur.execute("SELECT award_miles FROM member WHERE email = %s", [email])
        award_miles = cur.fetchone()[0]

        cur.execute(
            "SELECT id, harga_paket, jumlah_award_miles FROM award_miles_package ORDER BY harga_paket"
        )
        paket_list = [{'id': r[0], 'harga_paket': r[1], 'jumlah_award_miles': r[2]}
                      for r in cur.fetchall()]

        cur.execute("""
            SELECT map.id_award_miles_package, ap.jumlah_award_miles,
                   ap.harga_paket, map.timestamp
            FROM member_award_miles_package map
            JOIN award_miles_package ap ON map.id_award_miles_package = ap.id
            WHERE map.email_member = %s
            ORDER BY map.timestamp DESC
        """, [email])
        riwayat_beli       = []
        total_miles_dibeli = 0
        for r in cur.fetchall():
            riwayat_beli.append({
                'id_paket': r[0], 'jumlah_miles': r[1], 'harga': r[2], 'timestamp': r[3],
            })
            total_miles_dibeli += r[1]

    return render(request, 'package.html', {
        'role':         'member',
        'award_miles':  award_miles,
        'paket_list':   paket_list,
        'riwayat_beli': riwayat_beli,
        'stats': {
            'total_beli':   len(riwayat_beli),
            'miles_dibeli': total_miles_dibeli,
        },
        'success_msg': request.session.pop('success_msg', None),
        'error_msg':   request.session.pop('error_msg', None),
    })


def package_beli(request):
    role = request.session.get('role')
    if not role or role != 'member' or request.method != 'POST':
        return redirect('beli_package')

    email    = request.session.get('email')
    id_paket = request.POST.get('id_paket', '').strip()

    with connection.cursor() as cur:
        cur.execute(
            "SELECT jumlah_award_miles, harga_paket FROM award_miles_package WHERE id = %s",
            [id_paket]
        )
        paket = cur.fetchone()

    if not paket:
        request.session['error_msg'] = 'Paket tidak ditemukan.'
        return redirect('beli_package')

    jumlah_miles, _ = paket

    try:
        with transaction.atomic():
            with connection.cursor() as cur:
                cur.execute("""
                    INSERT INTO member_award_miles_package (id_award_miles_package, email_member, timestamp)
                    VALUES (%s, %s, NOW())
                """, [id_paket, email])
        request.session['success_msg'] = (
            f'SUKSES: Pembelian package berhasil. '
            f'Award miles dan total miles Anda bertambah {jumlah_miles} miles.'
        )
    except Exception as e:
        request.session['error_msg'] = _extract_raise_message(e)

    return redirect('beli_package')


# ─── KELOLA MEMBER (STAF) ─────────────────────────────────────────────────────

def kelola_member(request):
    role = request.session.get('role')
    if not role or role != 'staf':
        return redirect('login')

    search      = request.GET.get('search', '').strip()
    tier_filter = request.GET.get('tier', 'semua')

    with connection.cursor() as cur:
        params     = []
        conditions = ["1=1"]

        if search:
            conditions.append("""(
                LOWER(p.first_mid_name) LIKE %s OR LOWER(p.last_name) LIKE %s
                OR LOWER(m.email) LIKE %s OR LOWER(m.nomor_member) LIKE %s
            )""")
            s = f'%{search.lower()}%'
            params += [s, s, s, s]
        if tier_filter != 'semua':
            conditions.append("t.nama = %s")
            params.append(tier_filter)

        where_clause = " AND ".join(conditions)
        cur.execute(f"""
            SELECT m.nomor_member,
                   p.salutation || ' ' || p.first_mid_name || ' ' || p.last_name AS nama,
                   m.email, t.nama AS tier, m.total_miles, m.award_miles,
                   m.tanggal_bergabung
            FROM member m
            JOIN pengguna p ON m.email = p.email
            JOIN tier     t ON m.id_tier = t.id_tier
            WHERE {where_clause}
            ORDER BY m.nomor_member
        """, params)
        rows = cur.fetchall()
        member_list = [
            {
                'nomor_member': r[0], 'nama': r[1], 'email': r[2],
                'tier': r[3], 'total_miles': r[4], 'award_miles': r[5],
                'tanggal_bergabung': r[6],
            }
            for r in rows
        ]

        cur.execute("SELECT id_tier, nama FROM tier ORDER BY minimal_tier_miles")
        tier_list = cur.fetchall()

        cur.execute("""
            SELECT COUNT(*), COALESCE(SUM(total_miles), 0), COALESCE(SUM(award_miles), 0)
            FROM member
        """)
        total_member, total_miles_semua, total_award_miles = cur.fetchone()

        cur.execute("""
            SELECT t.nama, COUNT(m.email)
            FROM tier t
            LEFT JOIN member m ON m.id_tier = t.id_tier
            GROUP BY t.id_tier, t.nama, t.minimal_tier_miles
            ORDER BY t.minimal_tier_miles DESC
            LIMIT 1
        """)
        top_tier_row = cur.fetchone()

        cur.execute("""
            SELECT m.nomor_member,
                   p.salutation || ' ' || p.first_mid_name || ' ' || p.last_name AS nama,
                   t.nama AS tier,
                   m.tanggal_bergabung
            FROM member m
            JOIN pengguna p ON m.email = p.email
            JOIN tier t ON m.id_tier = t.id_tier
            ORDER BY m.tanggal_bergabung DESC, m.nomor_member DESC
            LIMIT 1
        """)
        latest_member_row = cur.fetchone()

    return render(request, 'kelola_member.html', {
        'role': 'staf', 'member_list': member_list,
        'tier_list': tier_list, 'search': search, 'tier_filter': tier_filter,
        'total_member': total_member,
        'total_miles_semua': total_miles_semua,
        'total_award_miles': total_award_miles,
        'top_tier': {
            'nama': top_tier_row[0],
            'jumlah': top_tier_row[1],
        } if top_tier_row else None,
        'latest_member': {
            'nomor_member': latest_member_row[0],
            'nama': latest_member_row[1],
            'tier': latest_member_row[2],
            'tanggal_bergabung': latest_member_row[3],
        } if latest_member_row else None,
        'success_msg': request.session.pop('success_msg', None),
        'error_msg':   request.session.pop('error_msg', None),
    })


def member_tambah(request):
    role = request.session.get('role')
    if not role or role != 'staf' or request.method != 'POST':
        return redirect('kelola_member')

    email           = normalize_email(request.POST.get('email', ''))
    password        = request.POST.get('password', '').strip()

    if not email or not password:
        request.session['error_msg'] = 'Semua field wajib diisi.'
        return redirect('kelola_member')

    err = _validate_max_length(email, 100, 'Email')
    if err:
        request.session['error_msg'] = err
        return redirect('kelola_member')

    if len(password) < 8:
        request.session['error_msg'] = 'Password minimal 8 karakter.'
        return redirect('kelola_member')

    valid, result = validate_profil_data(request.POST)
    if not valid:
        request.session['error_msg'] = result
        return redirect('kelola_member')
    data = result

    try:
        with transaction.atomic():
            with connection.cursor() as cur:
                cur.execute(
                    "SELECT 1 FROM pengguna WHERE LOWER(email) = LOWER(%s)", [email]
                )
                if cur.fetchone():
                    request.session['error_msg'] = f'Email {email} sudah terdaftar.'
                    return redirect('kelola_member')

                cur.execute("SELECT 1 FROM pengguna WHERE mobile_number = %s", [data['mobile_number']])
                if cur.fetchone():
                    request.session['error_msg'] = 'Nomor HP sudah digunakan.'
                    return redirect('kelola_member')

                cur.execute("""
                    INSERT INTO pengguna (email, password, salutation, first_mid_name, last_name,
                                         country_code, mobile_number, tanggal_lahir, kewarganegaraan)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """, [email, hash_password(password), data['salutation'], data['first_mid'],
                      data['last_name'], data['country_code'], data['mobile_number'],
                      data['tanggal_lahir'], data['kewarganegaraan']])

                cur.execute(
                    "SELECT id_tier FROM tier ORDER BY minimal_tier_miles ASC LIMIT 1"
                )
                tier_id = cur.fetchone()[0]

                cur.execute("""
                    INSERT INTO member (email, tanggal_bergabung, id_tier,
                                        award_miles, total_miles)
                    VALUES (%s,%s,%s,0,0)
                    RETURNING nomor_member
                """, [email, date.today(), tier_id])
                nomor_member = cur.fetchone()[0]

        request.session['success_msg'] = f'Member {nomor_member} berhasil ditambahkan.'
    except Exception as e:
        request.session['error_msg'] = f'Gagal: {_extract_raise_message(e)}'

    return redirect('kelola_member')


def member_edit(request, email_member):
    role = request.session.get('role')
    if not role or role != 'staf' or request.method != 'POST':
        return redirect('kelola_member')

    id_tier         = request.POST.get('id_tier', '').strip()

    valid, result = validate_profil_data(request.POST)
    if not valid:
        request.session['error_msg'] = result
        return redirect('kelola_member')
    data = result

    try:
        with transaction.atomic():
            with connection.cursor() as cur:
                if id_tier and not _row_exists(cur, 'tier', 'id_tier', id_tier):
                    request.session['error_msg'] = 'Tier tidak valid.'
                    return redirect('kelola_member')

                cur.execute("""
                    UPDATE pengguna SET salutation=%s, first_mid_name=%s, last_name=%s,
                        country_code=%s, mobile_number=%s, tanggal_lahir=%s, kewarganegaraan=%s
                    WHERE email=%s
                """, [data['salutation'], data['first_mid'], data['last_name'],
                      data['country_code'], data['mobile_number'], data['tanggal_lahir'],
                      data['kewarganegaraan'], email_member])

                if id_tier:
                    cur.execute(
                        "UPDATE member SET id_tier=%s WHERE email=%s", [id_tier, email_member]
                    )

        request.session['success_msg'] = 'Data member berhasil diperbarui.'
    except Exception as e:
        request.session['error_msg'] = f'Gagal: {_extract_raise_message(e)}'

    return redirect('kelola_member')


def member_hapus(request, email_member):
    role = request.session.get('role')
    if not role or role != 'staf' or request.method != 'POST':
        return redirect('kelola_member')

    try:
        with transaction.atomic():
            with connection.cursor() as cur:
                cur.execute("DELETE FROM pengguna WHERE email = %s", [email_member])
        request.session['success_msg'] = f'Member {email_member} berhasil dihapus.'
    except Exception as e:
        request.session['error_msg'] = f'Gagal: {_extract_raise_message(e)}'

    return redirect('kelola_member')


# ─── KELOLA HADIAH & PENYEDIA (STAF) ─────────────────────────────────────────

def kelola_hadiah(request):
    role = request.session.get('role')
    if not role or role != 'staf':
        return redirect('login')

    penyedia_filter = request.GET.get('penyedia', 'semua')
    status_filter   = request.GET.get('status', 'semua')
    search          = request.GET.get('search', '').strip()

    with connection.cursor() as cur:
        params     = []
        conditions = ["1=1"]

        if penyedia_filter != 'semua':
            conditions.append("h.id_penyedia = %s")
            params.append(penyedia_filter)
        if status_filter == 'aktif':
            conditions.append(
                "h.program_end >= CURRENT_DATE AND h.valid_start_date <= CURRENT_DATE"
            )
        elif status_filter == 'expired':
            conditions.append(
                "(h.program_end < CURRENT_DATE OR h.valid_start_date > CURRENT_DATE)"
            )
        if search:
            conditions.append("LOWER(h.nama) LIKE %s")
            params.append(f'%{search.lower()}%')

        where_clause = " AND ".join(conditions)
        cur.execute(f"""
            SELECT h.kode_hadiah, h.nama, h.miles, h.deskripsi,
                   h.valid_start_date, h.program_end, h.id_penyedia,
                   COALESCE(m.nama_maskapai, mt.nama_mitra, 'Penyedia #' || p.id::text) AS nama_penyedia,
                   CASE WHEN m.kode_maskapai IS NOT NULL THEN 'airline' ELSE 'partner' END AS tipe_penyedia,
                   CASE WHEN h.program_end >= CURRENT_DATE AND h.valid_start_date <= CURRENT_DATE
                        THEN true ELSE false END AS is_active,
                   h.program_end - CURRENT_DATE AS days_remaining,
                   COALESCE(rc.total_redeem, 0) AS total_redeem,
                   rc.latest_redeem
            FROM hadiah h
            JOIN penyedia p ON p.id = h.id_penyedia
            LEFT JOIN maskapai m ON m.id_penyedia = p.id
            LEFT JOIN mitra mt ON mt.id_penyedia = p.id
            LEFT JOIN (
                SELECT kode_hadiah, COUNT(*) AS total_redeem, MAX(timestamp) AS latest_redeem
                FROM redeem
                GROUP BY kode_hadiah
            ) rc ON rc.kode_hadiah = h.kode_hadiah
            WHERE {where_clause}
            ORDER BY h.kode_hadiah
        """, params)
        hadiah_list = []
        for r in cur.fetchall():
            hadiah_list.append({
                'kode_hadiah': r[0], 'nama': r[1], 'miles': r[2], 'deskripsi': r[3],
                'valid_start_date': r[4], 'program_end': r[5], 'id_penyedia': r[6],
                'nama_penyedia': r[7], 'tipe_penyedia': r[8], 'is_active': r[9],
                'days_remaining': r[10], 'total_redeem': r[11], 'latest_redeem': r[12],
            })

        cur.execute("SELECT COUNT(*) FROM hadiah")
        total_hadiah = cur.fetchone()[0]
        cur.execute("""
            SELECT COUNT(*) FROM hadiah
            WHERE program_end >= CURRENT_DATE AND valid_start_date <= CURRENT_DATE
        """)
        total_aktif = cur.fetchone()[0]
        cur.execute("SELECT COALESCE(COUNT(*), 0) FROM redeem")
        total_redeem = cur.fetchone()[0]
        cur.execute("SELECT COALESCE(ROUND(AVG(miles))::int, 0) FROM hadiah")
        avg_miles = cur.fetchone()[0]
        cur.execute("""
            SELECT h.kode_hadiah, h.nama, COUNT(r.kode_hadiah) AS total_redeem
            FROM hadiah h
            LEFT JOIN redeem r ON r.kode_hadiah = h.kode_hadiah
            GROUP BY h.kode_hadiah, h.nama
            ORDER BY total_redeem DESC, h.kode_hadiah
            LIMIT 1
        """)
        top_row = cur.fetchone()
        top_reward = None
        if top_row:
            top_reward = {
                'kode_hadiah': top_row[0],
                'nama': top_row[1],
                'total_redeem': top_row[2],
            }

        cur.execute("""
            SELECT p.id,
                   COALESCE(m.nama_maskapai, mt.nama_mitra, 'Penyedia #' || p.id::text) AS nama,
                   CASE WHEN m.kode_maskapai IS NOT NULL THEN 'airline' ELSE 'partner' END AS tipe
            FROM penyedia p
            LEFT JOIN maskapai m  ON m.id_penyedia = p.id
            LEFT JOIN mitra    mt ON mt.id_penyedia = p.id
            ORDER BY p.id
        """)
        penyedia_list = [{'id': r[0], 'nama': r[1], 'tipe': r[2]} for r in cur.fetchall()]

    return render(request, 'kelola_hadiah.html', {
        'role': 'staf', 'hadiah_list': hadiah_list,
        'penyedia_list': penyedia_list,
        'stats': {
            'total': total_hadiah, 'aktif': total_aktif,
            'expired': total_hadiah - total_aktif,
            'penyedia': len(penyedia_list),
            'total_redeem': total_redeem,
            'avg_miles': avg_miles,
            'top_reward': top_reward,
        },
        'penyedia_filter': penyedia_filter, 'status_filter': status_filter,
        'search': search,
        'success_msg': request.session.pop('success_msg', None),
        'error_msg':   request.session.pop('error_msg', None),
    })


def hadiah_tambah(request):
    role = request.session.get('role')
    if not role or role != 'staf' or request.method != 'POST':
        return redirect('kelola_hadiah')

    nama        = request.POST.get('nama', '').strip()
    deskripsi   = request.POST.get('deskripsi', '').strip() or None
    id_penyedia = request.POST.get('id_penyedia', '').strip()
    miles       = request.POST.get('miles', '').strip()
    valid_start = request.POST.get('valid_start_date', '').strip()
    program_end = request.POST.get('program_end', '').strip()

    if not all([nama, id_penyedia, miles, valid_start, program_end]):
        request.session['error_msg'] = 'Semua field wajib diisi.'
        return redirect('kelola_hadiah')

    err = _validate_max_length(nama, 100, 'Nama hadiah')
    if err:
        request.session['error_msg'] = err
        return redirect('kelola_hadiah')

    miles_int, err = _validate_positive_int(miles, 'Miles')
    if err:
        request.session['error_msg'] = err
        return redirect('kelola_hadiah')
    id_penyedia_int, err = _validate_positive_int(id_penyedia, 'Penyedia')
    if err:
        request.session['error_msg'] = err
        return redirect('kelola_hadiah')
    valid_start_date, err = _parse_date(valid_start, 'tanggal mulai')
    if err:
        request.session['error_msg'] = err
        return redirect('kelola_hadiah')
    program_end_date, err = _parse_date(program_end, 'tanggal selesai')
    if err:
        request.session['error_msg'] = err
        return redirect('kelola_hadiah')
    if program_end_date <= valid_start_date:
        request.session['error_msg'] = 'Tanggal selesai harus lebih akhir dari tanggal mulai.'
        return redirect('kelola_hadiah')

    try:
        with transaction.atomic():
            with connection.cursor() as cur:
                if not _row_exists(cur, 'penyedia', 'id', id_penyedia_int):
                    request.session['error_msg'] = 'Penyedia tidak valid.'
                    return redirect('kelola_hadiah')

                cur.execute("""
                    INSERT INTO hadiah (nama, miles, deskripsi,
                                        valid_start_date, program_end, id_penyedia)
                    VALUES (%s,%s,%s,%s,%s,%s)
                    RETURNING kode_hadiah
                """, [nama, miles_int, deskripsi, valid_start_date, program_end_date, id_penyedia_int])
                kode = cur.fetchone()[0]

        request.session['success_msg'] = f'Hadiah {kode} berhasil ditambahkan.'
    except Exception as e:
        request.session['error_msg'] = f'Gagal: {_extract_raise_message(e)}'

    return redirect('kelola_hadiah')


def hadiah_edit(request, kode):
    role = request.session.get('role')
    if not role or role != 'staf' or request.method != 'POST':
        return redirect('kelola_hadiah')

    nama        = request.POST.get('nama', '').strip()
    deskripsi   = request.POST.get('deskripsi', '').strip() or None
    id_penyedia = request.POST.get('id_penyedia', '').strip()
    miles       = request.POST.get('miles', '').strip()
    valid_start = request.POST.get('valid_start_date', '').strip()
    program_end = request.POST.get('program_end', '').strip()

    if not all([nama, id_penyedia, miles, valid_start, program_end]):
        request.session['error_msg'] = 'Semua field wajib diisi.'
        return redirect('kelola_hadiah')

    err = _validate_max_length(nama, 100, 'Nama hadiah')
    if err:
        request.session['error_msg'] = err
        return redirect('kelola_hadiah')
    miles_int, err = _validate_positive_int(miles, 'Miles')
    if err:
        request.session['error_msg'] = err
        return redirect('kelola_hadiah')
    id_penyedia_int, err = _validate_positive_int(id_penyedia, 'Penyedia')
    if err:
        request.session['error_msg'] = err
        return redirect('kelola_hadiah')
    valid_start_date, err = _parse_date(valid_start, 'tanggal mulai')
    if err:
        request.session['error_msg'] = err
        return redirect('kelola_hadiah')
    program_end_date, err = _parse_date(program_end, 'tanggal selesai')
    if err:
        request.session['error_msg'] = err
        return redirect('kelola_hadiah')
    if program_end_date <= valid_start_date:
        request.session['error_msg'] = 'Tanggal selesai harus lebih akhir dari tanggal mulai.'
        return redirect('kelola_hadiah')

    try:
        with transaction.atomic():
            with connection.cursor() as cur:
                if not _row_exists(cur, 'penyedia', 'id', id_penyedia_int):
                    request.session['error_msg'] = 'Penyedia tidak valid.'
                    return redirect('kelola_hadiah')

                cur.execute("""
                    UPDATE hadiah SET nama=%s, deskripsi=%s, id_penyedia=%s,
                        miles=%s, valid_start_date=%s, program_end=%s
                    WHERE kode_hadiah=%s
                """, [nama, deskripsi, id_penyedia_int, miles_int, valid_start_date, program_end_date, kode])
        request.session['success_msg'] = f'Hadiah {kode} berhasil diperbarui.'
    except Exception as e:
        request.session['error_msg'] = f'Gagal: {_extract_raise_message(e)}'

    return redirect('kelola_hadiah')


def hadiah_hapus(request, kode):
    role = request.session.get('role')
    if not role or role != 'staf' or request.method != 'POST':
        return redirect('kelola_hadiah')

    with connection.cursor() as cur:
        cur.execute("SELECT program_end FROM hadiah WHERE kode_hadiah = %s", [kode])
        row = cur.fetchone()

    if not row:
        request.session['error_msg'] = 'Hadiah tidak ditemukan.'
        return redirect('kelola_hadiah')
    if row[0] >= date.today():
        request.session['error_msg'] = 'Hadiah aktif tidak bisa dihapus.'
        return redirect('kelola_hadiah')

    try:
        with transaction.atomic():
            with connection.cursor() as cur:
                cur.execute("DELETE FROM hadiah WHERE kode_hadiah = %s", [kode])
        request.session['success_msg'] = f'Hadiah {kode} berhasil dihapus.'
    except Exception as e:
        request.session['error_msg'] = f'Gagal: {_extract_raise_message(e)}'

    return redirect('kelola_hadiah')


# ─── KELOLA MITRA (STAF) ─────────────────────────────────────────────────────

def kelola_mitra(request):
    role = request.session.get('role')
    if not role or role != 'staf':
        return redirect('login')

    search = request.GET.get('search', '').strip()

    with connection.cursor() as cur:
        params     = []
        conditions = ["1=1"]

        if search:
            conditions.append(
                "(LOWER(mt.nama_mitra) LIKE %s OR LOWER(mt.email_mitra) LIKE %s)"
            )
            s = f'%{search.lower()}%'
            params += [s, s]

        where_clause = " AND ".join(conditions)
        cur.execute(f"""
            SELECT mt.email_mitra, mt.id_penyedia, mt.nama_mitra, mt.tanggal_kerja_sama
            FROM mitra mt
            WHERE {where_clause}
            ORDER BY mt.nama_mitra
        """, params)
        mitra_list = [
            {'email_mitra': r[0], 'id_penyedia': r[1], 'nama_mitra': r[2],
             'tanggal_kerja_sama': r[3]}
            for r in cur.fetchall()
        ]

        cur.execute("SELECT COUNT(*) FROM mitra")
        total = cur.fetchone()[0]

    return render(request, 'kelola_mitra.html', {
        'role': 'staf', 'mitra_list': mitra_list,
        'search': search,
        'stats': {'total': total},
        'success_msg': request.session.pop('success_msg', None),
        'error_msg':   request.session.pop('error_msg', None),
    })


def mitra_tambah(request):
    role = request.session.get('role')
    if not role or role != 'staf' or request.method != 'POST':
        return redirect('kelola_mitra')

    email_mitra        = normalize_email(request.POST.get('email_mitra', ''))
    nama_mitra         = request.POST.get('nama_mitra', '').strip()
    tanggal_kerja_sama = request.POST.get('tanggal_kerja_sama', '').strip()

    if not all([email_mitra, nama_mitra, tanggal_kerja_sama]):
        request.session['error_msg'] = 'Semua field wajib diisi.'
        return redirect('kelola_mitra')

    for value, max_length, label in (
        (email_mitra, 100, 'Email mitra'),
        (nama_mitra, 100, 'Nama mitra'),
    ):
        err = _validate_max_length(value, max_length, label)
        if err:
            request.session['error_msg'] = err
            return redirect('kelola_mitra')

    tanggal_kerja_sama_date, err = _parse_date(tanggal_kerja_sama, 'tanggal kerja sama')
    if err:
        request.session['error_msg'] = err
        return redirect('kelola_mitra')

    with connection.cursor() as cur:
        cur.execute("SELECT 1 FROM mitra WHERE email_mitra = %s", [email_mitra])
        if cur.fetchone():
            request.session['error_msg'] = f'Email mitra {email_mitra} sudah terdaftar.'
            return redirect('kelola_mitra')

    try:
        with transaction.atomic():
            with connection.cursor() as cur:
                cur.execute("INSERT INTO penyedia DEFAULT VALUES RETURNING id")
                new_penyedia_id = cur.fetchone()[0]

                cur.execute("""
                    INSERT INTO mitra (email_mitra, id_penyedia, nama_mitra, tanggal_kerja_sama)
                    VALUES (%s,%s,%s,%s)
                """, [email_mitra, new_penyedia_id, nama_mitra, tanggal_kerja_sama_date])

        request.session['success_msg'] = (
            f'Mitra "{nama_mitra}" berhasil ditambahkan (ID Penyedia: {new_penyedia_id}).'
        )
    except Exception as e:
        request.session['error_msg'] = f'Gagal: {_extract_raise_message(e)}'

    return redirect('kelola_mitra')


def mitra_edit(request, email_mitra):
    role = request.session.get('role')
    if not role or role != 'staf' or request.method != 'POST':
        return redirect('kelola_mitra')

    nama_baru = request.POST.get('nama_mitra', '').strip()
    tgl_baru  = request.POST.get('tanggal_kerja_sama', '').strip()

    if not nama_baru or not tgl_baru:
        request.session['error_msg'] = 'Nama dan tanggal wajib diisi.'
        return redirect('kelola_mitra')

    err = _validate_max_length(nama_baru, 100, 'Nama mitra')
    if err:
        request.session['error_msg'] = err
        return redirect('kelola_mitra')
    tgl_baru_date, err = _parse_date(tgl_baru, 'tanggal kerja sama')
    if err:
        request.session['error_msg'] = err
        return redirect('kelola_mitra')

    try:
        with transaction.atomic():
            with connection.cursor() as cur:
                cur.execute("""
                    UPDATE mitra SET nama_mitra=%s, tanggal_kerja_sama=%s WHERE email_mitra=%s
                """, [nama_baru, tgl_baru_date, email_mitra])
        request.session['success_msg'] = f'Mitra "{nama_baru}" berhasil diperbarui.'
    except Exception as e:
        request.session['error_msg'] = f'Gagal: {_extract_raise_message(e)}'

    return redirect('kelola_mitra')


def mitra_hapus(request, email_mitra):
    role = request.session.get('role')
    if not role or role != 'staf' or request.method != 'POST':
        return redirect('kelola_mitra')

    with connection.cursor() as cur:
        cur.execute("SELECT id_penyedia FROM mitra WHERE email_mitra=%s", [email_mitra])
        row = cur.fetchone()

    if not row:
        request.session['error_msg'] = 'Mitra tidak ditemukan.'
        return redirect('kelola_mitra')

    id_penyedia = row[0]

    try:
        with transaction.atomic():
            with connection.cursor() as cur:
                cur.execute("DELETE FROM mitra WHERE email_mitra = %s", [email_mitra])
                cur.execute("DELETE FROM penyedia WHERE id = %s", [id_penyedia])
        request.session['success_msg'] = 'Mitra berhasil dihapus beserta hadiah terkait.'
    except Exception as e:
        request.session['error_msg'] = f'Gagal: {_extract_raise_message(e)}'

    return redirect('kelola_mitra')


# ─── LAPORAN TRANSAKSI (STAF) ─────────────────────────────────────────────────

def laporan_transaksi(request):
    role = request.session.get('role')
    if not role or role != 'staf':
        return redirect('login')

    search     = request.GET.get('search', '').strip()
    tgl_dari   = request.GET.get('tgl_dari', '').strip()
    tgl_sampai = request.GET.get('tgl_sampai', '').strip()
    active_tab = request.GET.get('tab', 'klaim')
    if tgl_dari and _parse_date(tgl_dari, 'tanggal dari')[1]:
        tgl_dari = ''
    if tgl_sampai and _parse_date(tgl_sampai, 'tanggal sampai')[1]:
        tgl_sampai = ''
    if active_tab not in {'klaim', 'transfer', 'redeem', 'beli'}:
        active_tab = 'klaim'

    def build_date_conditions(alias, col='timestamp'):
        conds  = []
        params = []
        if tgl_dari:
            conds.append(f"{alias}.{col}::date >= %s")
            params.append(tgl_dari)
        if tgl_sampai:
            conds.append(f"{alias}.{col}::date <= %s")
            params.append(tgl_sampai)
        return conds, params

    def build_member_conditions(alias, email_col):
        if not search:
            return [], []
        s = f'%{search.lower()}%'
        return (
            [f"(LOWER({alias}.{email_col}) LIKE %s OR LOWER(p.first_mid_name) LIKE %s OR LOWER(p.last_name) LIKE %s)"],
            [s, s, s],
        )

    with connection.cursor() as cur:
        # ── KLAIM ──────────────────────────────────────────────────────────
        conds, params = ["1=1"], []
        dc, dp = build_date_conditions('c')
        mc, mp = build_member_conditions('c', 'email_member')
        conds += dc + mc; params += dp + mp
        cur.execute(f"""
            SELECT c.id, p.first_mid_name || ' ' || p.last_name, c.email_member,
                   mk.nama_maskapai, c.bandara_asal, c.bandara_tujuan,
                   c.kelas_kabin, c.status_penerimaan, c.timestamp, c.email_staf
            FROM claim_missing_miles c
            JOIN pengguna p  ON c.email_member = p.email
            JOIN maskapai mk ON c.maskapai = mk.kode_maskapai
            WHERE {' AND '.join(conds)}
            ORDER BY c.timestamp DESC
        """, params)
        klaim_list = [
            {
                'id': r[0], 'nama_member': r[1], 'email_member': r[2],
                'maskapai': r[3], 'rute': f"{r[4]} → {r[5]}",
                'kelas_kabin': r[6], 'status': r[7], 'timestamp': r[8],
                'email_staf': r[9],
            }
            for r in cur.fetchall()
        ]

        # ── TRANSFER ───────────────────────────────────────────────────────
        conds, params = ["1=1"], []
        dc, dp = build_date_conditions('t')
        mc, mp = build_member_conditions('t', 'email_member_1')
        conds += dc + mc; params += dp + mp
        cur.execute(f"""
            SELECT t.email_member_1,
                   p1.first_mid_name || ' ' || p1.last_name,
                   t.email_member_2,
                   p2.first_mid_name || ' ' || p2.last_name,
                   t.jumlah, t.catatan, t.timestamp
            FROM transfer t
            JOIN pengguna p1 ON t.email_member_1 = p1.email
            JOIN pengguna p2 ON t.email_member_2 = p2.email
            JOIN pengguna p  ON p.email = t.email_member_1
            WHERE {' AND '.join(conds)}
            ORDER BY t.timestamp DESC
        """, params)
        transfer_list = [
            {
                'email_dari': r[0], 'nama_dari': r[1],
                'email_ke': r[2], 'nama_ke': r[3],
                'jumlah': r[4], 'catatan': r[5], 'timestamp': r[6],
            }
            for r in cur.fetchall()
        ]

        # ── REDEEM ─────────────────────────────────────────────────────────
        conds, params = ["1=1"], []
        dc, dp = build_date_conditions('r')
        mc, mp = build_member_conditions('r', 'email_member')
        conds += dc + mc; params += dp + mp
        cur.execute(f"""
            SELECT r.email_member, p.first_mid_name || ' ' || p.last_name,
                   r.kode_hadiah, h.nama, h.miles, r.timestamp
            FROM redeem r
            JOIN pengguna p ON r.email_member = p.email
            JOIN hadiah   h ON r.kode_hadiah  = h.kode_hadiah
            WHERE {' AND '.join(conds)}
            ORDER BY r.timestamp DESC
        """, params)
        redeem_list = [
            {
                'email': r[0], 'nama': r[1], 'kode_hadiah': r[2],
                'nama_hadiah': r[3], 'miles': r[4], 'timestamp': r[5],
            }
            for r in cur.fetchall()
        ]

        # ── BELI PACKAGE ───────────────────────────────────────────────────
        conds, params = ["1=1"], []
        dc, dp = build_date_conditions('map')
        mc, mp = build_member_conditions('map', 'email_member')
        conds += dc + mc; params += dp + mp
        cur.execute(f"""
            SELECT map.email_member, p.first_mid_name || ' ' || p.last_name,
                   map.id_award_miles_package, ap.jumlah_award_miles,
                   ap.harga_paket, map.timestamp
            FROM member_award_miles_package map
            JOIN pengguna p ON map.email_member = p.email
            JOIN award_miles_package ap ON map.id_award_miles_package = ap.id
            WHERE {' AND '.join(conds)}
            ORDER BY map.timestamp DESC
        """, params)
        beli_list = [
            {
                'email': r[0], 'nama': r[1], 'id_paket': r[2],
                'jumlah_miles': r[3], 'harga': r[4], 'timestamp': r[5],
            }
            for r in cur.fetchall()
        ]

        # ── STATS ──────────────────────────────────────────────────────────
        cur.execute("SELECT COALESCE(SUM(total_miles),0) FROM member")
        total_miles_beredar = cur.fetchone()[0]

        cur.execute("""
            SELECT COUNT(*) FROM redeem
            WHERE DATE_TRUNC('month', timestamp) = DATE_TRUNC('month', CURRENT_DATE)
        """)
        redeem_bulan_ini = cur.fetchone()[0]

        cur.execute(
            "SELECT COUNT(*) FROM claim_missing_miles WHERE status_penerimaan = 'Disetujui'"
        )
        klaim_disetujui = cur.fetchone()[0]

        # ── TOP 5 ──────────────────────────────────────────────────────────
        try:
            cur.execute("SELECT * FROM get_top5_member_by_miles()")
            top5_rows = cur.fetchall()
            top5_list = [
                {'rank': i + 1, 'email': r[0], 'nama': r[1], 'total_miles': r[2]}
                for i, r in enumerate(top5_rows)
            ]
            if top5_rows and len(top5_rows[0]) > 3 and top5_rows[0][3]:
                request.session['success_msg_laporan'] = top5_rows[0][3]
        except Exception:
            cur.execute("""
                SELECT m.email, p.first_mid_name || ' ' || p.last_name, m.total_miles
                FROM member m JOIN pengguna p ON m.email = p.email
                ORDER BY m.total_miles DESC LIMIT 5
            """)
            top5_list = [
                {'rank': i + 1, 'email': r[0], 'nama': r[1], 'total_miles': r[2]}
                for i, r in enumerate(cur.fetchall())
            ]

    return render(request, 'laporan_transaksi.html', {
        'role':          'staf',
        'search':        search,
        'tgl_dari':      tgl_dari,
        'tgl_sampai':    tgl_sampai,
        'active_tab':    active_tab,
        'stats': {
            'total_klaim':         len(klaim_list),
            'total_transfer':      len(transfer_list),
            'total_redeem':        len(redeem_list),
            'total_beli':          len(beli_list),
            'total_miles_beredar': total_miles_beredar,
            'redeem_bulan_ini':    redeem_bulan_ini,
            'klaim_disetujui':     klaim_disetujui,
        },
        'klaim_list':    klaim_list,
        'transfer_list': transfer_list,
        'redeem_list':   redeem_list,
        'beli_list':     beli_list,
        'top5_list':     top5_list,
        'success_msg':   request.session.pop('success_msg', None),
        'error_msg':     request.session.pop('error_msg', None),
    })


def laporan_hapus(request):
    role = request.session.get('role')
    if not role or role != 'staf' or request.method != 'POST':
        return redirect('laporan_transaksi')

    tipe = request.POST.get('tipe', '').strip()

    try:
        with transaction.atomic():
            with connection.cursor() as cur:
                if tipe == 'transfer':
                    em1 = request.POST.get('email_member_1', '').strip()
                    em2 = request.POST.get('email_member_2', '').strip()
                    ts  = request.POST.get('timestamp', '').strip()
                    cur.execute(
                        "DELETE FROM transfer WHERE email_member_1=%s AND email_member_2=%s AND timestamp=%s",
                        [em1, em2, ts]
                    )
                elif tipe == 'redeem':
                    em = request.POST.get('email_member', '').strip()
                    kh = request.POST.get('kode_hadiah', '').strip()
                    ts = request.POST.get('timestamp', '').strip()
                    cur.execute(
                        "DELETE FROM redeem WHERE email_member=%s AND kode_hadiah=%s AND timestamp=%s",
                        [em, kh, ts]
                    )
                elif tipe == 'beli':
                    id_p = request.POST.get('id_award_miles_package', '').strip()
                    em   = request.POST.get('email_member', '').strip()
                    ts   = request.POST.get('timestamp', '').strip()
                    cur.execute(
                        "DELETE FROM member_award_miles_package WHERE id_award_miles_package=%s AND email_member=%s AND timestamp=%s",
                        [id_p, em, ts]
                    )
                else:
                    request.session['error_msg'] = 'Tipe transaksi tidak valid.'
                    return redirect('laporan_transaksi')

        request.session['success_msg'] = 'Riwayat transaksi berhasil dihapus.'
    except Exception as e:
        request.session['error_msg'] = f'Gagal: {_extract_raise_message(e)}'

    return redirect('laporan_transaksi')
