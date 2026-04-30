from django.shortcuts import render, redirect

# ─── DUMMY DATA ───────────────────────────────────────────────────────────────

DUMMY_BANDARA = [
    ('CGK', 'Soekarno-Hatta, Jakarta'),
    ('DPS', 'Ngurah Rai, Bali'),
    ('SUB', 'Juanda, Surabaya'),
    ('JOG', 'Adisutjipto, Yogyakarta'),
    ('MDC', 'Sam Ratulangi, Manado'),
    ('BPN', 'Sultan Aji Muhammad Sulaiman, Balikpapan'),
    ('PLM', 'Sultan Mahmud Badaruddin II, Palembang'),
    ('SIN', 'Changi, Singapore'),
    ('KUL', 'Kuala Lumpur International'),
    ('BKK', 'Suvarnabhumi, Bangkok'),
    ('NRT', 'Narita, Tokyo'),
    ('HKG', 'Hong Kong International'),
    ('ICN', 'Incheon, Seoul'),
    ('SYD', 'Kingsford Smith, Sydney'),
    ('DOH', 'Hamad, Doha'),
]

DUMMY_MASKAPAI = [
    ('GA', 'Garuda Indonesia'),
    ('QG', 'Citilink'),
    ('JT', 'Lion Air'),
    ('SJ', 'Sriwijaya Air'),
    ('ID', 'Batik Air'),
]

DUMMY_KELAS = ['Economy', 'Premium Economy', 'Business', 'First']

DUMMY_KLAIM = [
    {
        'id': 1,
        'email_member': 'john@example.com',
        'nomor_klaim': 'CLM-001',
        'maskapai': 'GA',
        'nama_maskapai': 'Garuda Indonesia',
        'bandara_asal': 'CGK',
        'bandara_tujuan': 'DPS',
        'tanggal_penerbangan': '2024-10-01',
        'flight_number': 'GA404',
        'nomor_tiket': 'TKT-001',
        'kelas_kabin': 'Business',
        'pnr': 'ABC123',
        'status_penerimaan': 'Disetujui',
        'timestamp': '2024-10-05 18:45:00',
        'email_staf': 'admin@aeromiles.com',
    },
    {
        'id': 2,
        'email_member': 'john@example.com',
        'nomor_klaim': 'CLM-002',
        'maskapai': 'QG',
        'nama_maskapai': 'Citilink',
        'bandara_asal': 'CGK',
        'bandara_tujuan': 'SUB',
        'tanggal_penerbangan': '2024-11-15',
        'flight_number': 'QG801',
        'nomor_tiket': 'TKT-002',
        'kelas_kabin': 'Economy',
        'pnr': 'DEF456',
        'status_penerimaan': 'Menunggu',
        'timestamp': '2024-11-20 18:45:00',
        'email_staf': None,
    },
    {
        'id': 3,
        'email_member': 'john@example.com',
        'nomor_klaim': 'CLM-003',
        'maskapai': 'ID',
        'nama_maskapai': 'Batik Air',
        'bandara_asal': 'CGK',
        'bandara_tujuan': 'BPN',
        'tanggal_penerbangan': '2025-01-10',
        'flight_number': 'ID7503',
        'nomor_tiket': 'TKT-003',
        'kelas_kabin': 'Premium Economy',
        'pnr': 'GHI789',
        'status_penerimaan': 'Ditolak',
        'timestamp': '2025-01-15 18:45:00',
        'email_staf': 'admin@aeromiles.com',
    },
    {
        'id': 4,
        'email_member': 'john@example.com',
        'nomor_klaim': 'CLM-004',
        'maskapai': 'GA',
        'nama_maskapai': 'Garuda Indonesia',
        'bandara_asal': 'DPS',
        'bandara_tujuan': 'CGK',
        'tanggal_penerbangan': '2025-03-02',
        'flight_number': 'GA401',
        'nomor_tiket': 'TKT-004',
        'kelas_kabin': 'Economy',
        'pnr': 'JKL012',
        'status_penerimaan': 'Menunggu',
        'timestamp': '2025-03-05 09:00:00',
        'email_staf': None,
    },
    # Klaim dari member lain (untuk tampilan staf)
    {
        'id': 5,
        'email_member': 'siti.nurhaliza@email.com',
        'nomor_klaim': 'CLM-005',
        'maskapai': 'JT',
        'nama_maskapai': 'Lion Air',
        'bandara_asal': 'CGK',
        'bandara_tujuan': 'SUB',
        'tanggal_penerbangan': '2024-12-01',
        'flight_number': 'JT021',
        'nomor_tiket': 'TKT-005',
        'kelas_kabin': 'Economy',
        'pnr': 'MNO345',
        'status_penerimaan': 'Menunggu',
        'timestamp': '2024-12-05 18:45:00',
        'email_staf': None,
    },
    {
        'id': 6,
        'email_member': 'budi.santoso@email.com',
        'nomor_klaim': 'CLM-006',
        'maskapai': 'SJ',
        'nama_maskapai': 'Sriwijaya Air',
        'bandara_asal': 'CGK',
        'bandara_tujuan': 'PLM',
        'tanggal_penerbangan': '2025-01-10',
        'flight_number': 'SJ201',
        'nomor_tiket': 'TKT-006',
        'kelas_kabin': 'Economy',
        'pnr': 'PQR678',
        'status_penerimaan': 'Ditolak',
        'timestamp': '2025-01-15 18:45:00',
        'email_staf': 'admin@aeromiles.com',
    },
    {
        'id': 7,
        'email_member': 'dewi.lestari@email.com',
        'nomor_klaim': 'CLM-007',
        'maskapai': 'ID',
        'nama_maskapai': 'Batik Air',
        'bandara_asal': 'CGK',
        'bandara_tujuan': 'MDC',
        'tanggal_penerbangan': '2025-02-20',
        'flight_number': 'ID6301',
        'nomor_tiket': 'TKT-007',
        'kelas_kabin': 'Business',
        'pnr': 'STU901',
        'status_penerimaan': 'Menunggu',
        'timestamp': '2025-02-25 10:30:00',
        'email_staf': None,
    },
    {
        'id': 8,
        'email_member': 'eka.putra@email.com',
        'nomor_klaim': 'CLM-008',
        'maskapai': 'GA',
        'nama_maskapai': 'Garuda Indonesia',
        'bandara_asal': 'SUB',
        'bandara_tujuan': 'CGK',
        'tanggal_penerbangan': '2025-03-15',
        'flight_number': 'GA302',
        'nomor_tiket': 'TKT-008',
        'kelas_kabin': 'First',
        'pnr': 'VWX012',
        'status_penerimaan': 'Disetujui',
        'timestamp': '2025-03-20 09:15:00',
        'email_staf': 'admin@aeromiles.com',
    },
]

DUMMY_MEMBER_INFO = {
    'john@example.com': {'nama': 'Mr. John William Doe', 'nomor_member': 'M0001', 'tier': 'Gold'},
    'siti.nurhaliza@email.com': {'nama': 'Mrs. Siti Nurhaliza', 'nomor_member': 'M0002', 'tier': 'Silver'},
    'budi.santoso@email.com': {'nama': 'Mr. Budi Santoso', 'nomor_member': 'M0003', 'tier': 'Bronze'},
    'dewi.lestari@email.com': {'nama': 'Ms. Dewi Lestari', 'nomor_member': 'M0004', 'tier': 'Bronze'},
    'eka.putra@email.com': {'nama': 'Mr. Eka Putra', 'nomor_member': 'M0005', 'tier': 'Silver'},
}


# ─── HELPERS ──────────────────────────────────────────────────────────────────

def get_nama_maskapai(kode):
    for k, n in DUMMY_MASKAPAI:
        if k == kode:
            return n
    return kode


def enrich_klaim(klaim_list):
    """Tambahkan field rute dan info member ke list klaim."""
    result = []
    for k in klaim_list:
        item = dict(k)
        item['rute'] = f"{k['bandara_asal']} → {k['bandara_tujuan']}"
        info = DUMMY_MEMBER_INFO.get(k['email_member'], {})
        item['nama_member'] = info.get('nama', k['email_member'])
        item['nomor_member'] = info.get('nomor_member', '-')
        result.append(item)
    return result


def next_klaim_id():
    if not DUMMY_KLAIM:
        return 1
    return max(k['id'] for k in DUMMY_KLAIM) + 1

# ─── VIEWS TAMBAHAN (dari merge) ─────────────────────────────────────────────

def landing(request):
    if request.session.get('role'):
        return redirect('dashboard')
    return render(request, 'landing.html', {'role': 'guest'})




def dashboard_staf(request):
    role = request.session.get('role')
    if not role:
        return redirect('login')
    return render(request, 'dashboard_staf.html', {'role': 'staf'})


def tier(request):
    role = request.session.get('role')
    if not role:
        return redirect('login')
    if role == 'staf':
        return redirect('dashboard')
    context = {
        'role': 'member',
        'nama': request.session.get('nama', 'Member'),
        'email': request.session.get('email', ''),
        'tier_saat_ini': {
            'nama': 'Gold',
            'minimal_frekuensi_terbang': 15,
            'minimal_tier_miles': 50000,
        },
        'progress': {
            'total_miles': 45000,
            'total_penerbangan': 12,
            'miles_needed': 35000,
            'progress_percentage': 56.25,
        },
        'tier_berikutnya': {
            'nama': 'Diamond',
            'minimal_frekuensi_terbang': 30,
            'minimal_tier_miles': 150000,
        },
        'semua_tier': [
            {'nama': 'Bronze', 'minimal_tier_miles': 0, 'warna': 'orange',
             'benefits': ['Akumulasi miles dasar', 'Akses penawaran khusus member']},
            {'nama': 'Silver', 'minimal_tier_miles': 10000, 'warna': 'gray',
             'benefits': ['Bonus miles 25%', 'Priority check-in', 'Akses lounge partner']},
            {'nama': 'Gold',   'minimal_tier_miles': 50000, 'warna': 'amber', 'is_current': True,
             'benefits': ['Bonus miles 50%', 'Priority boarding', 'Extra bagasi 10kg']},
            {'nama': 'Diamond','minimal_tier_miles': 150000,'warna': 'indigo',
             'benefits': ['Bonus miles 100%', 'Upgrade gratis', 'Extra bagasi 20kg']},
        ]
    }
    return render(request, 'tier.html', context)


def kelola_member(request):
    role = request.session.get('role')
    if not role or role != 'staf':
        return redirect('login')
    return render(request, 'kelola_member.html', {'role': 'staf'})

# ─── AUTH VIEWS ───────────────────────────────────────────────────────────────

def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        if email == 'john@example.com' and password == 'password':
            request.session['role'] = 'member'
            request.session['email'] = email
            request.session['nama'] = 'Mr. John William Doe'
            return redirect('dashboard')
        elif email == 'admin@aeromiles.com' and password == 'password':
            request.session['role'] = 'staf'
            request.session['email'] = email
            request.session['nama'] = 'Mr. Admin Aero'
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {
                'role': 'guest',
                'error': 'Email atau password salah!'
            })

    return render(request, 'login.html', {'role': 'guest'})


def logout_view(request):
    request.session.flush()
    return redirect('login')



def register(request):
    return render(request, 'register.html', {'role': 'guest'})


# ─── MAIN VIEWS ───────────────────────────────────────────────────────────────

def dashboard(request):
    role = request.session.get('role')
    if not role:
        return redirect('login')
    if role == 'staf':
        return render(request, 'dashboard_staf.html', {'role': 'staf'})
    return render(request, 'dashboard.html', {'role': 'member'})


# ─── DUMMY DATA PROFIL ───────────────────────────────────────────────────────
# Tambahkan ini di bagian DUMMY DATA (atas views.py, setelah DUMMY_MEMBER_INFO)

DUMMY_USERS = {
    'john@example.com': {
        'email':           'john@example.com',
        'salutation':      'Mr.',
        'first_mid_name':  'John William',
        'last_name':       'Doe',
        'kewarganegaraan': 'Indonesia',
        'country_code':    '+62',
        'mobile_number':   '81234567890',
        'tanggal_lahir':   '1990-05-15',
        # password disimpan plaintext untuk dummy (di production harus di-hash)
        'password':        'password',
    },
    'admin@aeromiles.com': {
        'email':           'admin@aeromiles.com',
        'salutation':      'Mr.',
        'first_mid_name':  'Admin',
        'last_name':       'Aero',
        'kewarganegaraan': 'Indonesia',
        'country_code':    '+62',
        'mobile_number':   '81111111111',
        'tanggal_lahir':   '1988-01-01',
        'password':        'password',
    },
}

DUMMY_MEMBERS = {
    'john@example.com': {
        'nomor_member':      'M0001',
        'tanggal_bergabung': '15 Januari 2024',
        'id_tier':           'Gold',
    },
}

DUMMY_STAFS = {
    'admin@aeromiles.com': {
        'id_staf':       'S0001',
        'kode_maskapai': 'GA',
    },
}


# ─── VIEWS PROFIL ─────────────────────────────────────────────────────────────
# Ganti fungsi profil() yang sudah ada dengan versi ini:

def profil(request):
    role = request.session.get('role')
    if not role:
        return redirect('login')

    email = request.session.get('email')
    user  = DUMMY_USERS.get(email, {})

    # Ambil data member/staf jika ada
    member = DUMMY_MEMBERS.get(email) if role == 'member' else None
    staf   = DUMMY_STAFS.get(email)   if role == 'staf'   else None

    # Flash dari update sebelumnya
    success_msg = request.session.pop('success_msg', None)
    error_msg   = request.session.pop('error_msg', None)

    context = {
        'role':           role,
        'user':           user,
        'member':         member,
        'staf':           staf,
        'maskapai_list':  DUMMY_MASKAPAI,   # sudah ada di views.py
        'success_msg':    success_msg,
        'error_msg':      error_msg,
    }
    return render(request, 'profil.html', context)


def profil_update(request):
    role = request.session.get('role')
    if not role:
        return redirect('login')

    if request.method != 'POST':
        return redirect('profil')

    email = request.session.get('email')
    user  = DUMMY_USERS.get(email)

    if not user:
        return redirect('login')

    # Ambil data dari form
    salutation      = request.POST.get('salutation', '').strip()
    first_name      = request.POST.get('first_name', '').strip()
    middle_name     = request.POST.get('middle_name', '').strip()
    last_name       = request.POST.get('last_name', '').strip()
    kewarganegaraan = request.POST.get('kewarganegaraan', '').strip()
    country_code    = request.POST.get('country_code', '').strip()
    mobile_number   = request.POST.get('mobile_number', '').strip()
    tanggal_lahir   = request.POST.get('tanggal_lahir', '').strip()

    # Validasi field wajib
    if not all([salutation, first_name, last_name, kewarganegaraan,
                country_code, mobile_number, tanggal_lahir]):
        request.session['error_msg'] = 'Semua field wajib diisi.'
        return redirect('profil')

    # Gabungkan first + middle name jadi first_mid_name
    first_mid = f"{first_name} {middle_name}".strip() if middle_name else first_name

    # Update dummy data (in-memory)
    user['salutation']      = salutation
    user['first_mid_name']  = first_mid
    user['last_name']       = last_name
    user['kewarganegaraan'] = kewarganegaraan
    user['country_code']    = country_code
    user['mobile_number']   = mobile_number
    user['tanggal_lahir']   = tanggal_lahir

    # Khusus staf: update kode maskapai
    if role == 'staf':
        staf = DUMMY_STAFS.get(email)
        if staf:
            kode_maskapai = request.POST.get('kode_maskapai', '').strip()
            if kode_maskapai:
                staf['kode_maskapai'] = kode_maskapai

    # Update nama di session supaya navbar ikut berubah
    request.session['nama'] = f"{salutation} {first_mid} {last_name}".strip()

    request.session['success_msg'] = 'Perubahan berhasil disimpan.'
    return redirect('profil')


def profil_ubah_password(request):
    role = request.session.get('role')
    if not role:
        return redirect('login')

    if request.method != 'POST':
        return redirect('profil')

    email = request.session.get('email')
    user  = DUMMY_USERS.get(email)

    if not user:
        return redirect('login')

    password_lama  = request.POST.get('password_lama', '')
    password_baru  = request.POST.get('password_baru', '')
    konfirmasi     = request.POST.get('konfirmasi_password', '')

    # Validasi password lama (dummy: plaintext)
    if password_lama != user['password']:
        request.session['error_msg'] = 'Password lama tidak sesuai.'
        return redirect('profil')

    if not password_baru:
        request.session['error_msg'] = 'Password baru tidak boleh kosong.'
        return redirect('profil')

    if password_baru != konfirmasi:
        request.session['error_msg'] = 'Konfirmasi password tidak cocok.'
        return redirect('profil')

    if len(password_baru) < 8:
        request.session['error_msg'] = 'Password baru minimal 8 karakter.'
        return redirect('profil')

    # Update password di dummy data
    user['password'] = password_baru

    request.session['success_msg'] = 'Password berhasil diubah.'
    return redirect('profil')


def identitas(request):
    role = request.session.get('role')
    if not role:
        return redirect('login')
    return render(request, 'identitas.html', {'role': 'member'})


# ─── FITUR 8: KLAIM MISSING MILES – MEMBER (CRUD) ────────────────────────────

def klaim_member(request):
    """R — Daftar klaim milik member yang sedang login."""
    role = request.session.get('role')
    if not role or role != 'member':
        return redirect('login')

    email = request.session.get('email')
    status_filter = request.GET.get('status', 'semua')

    klaim_saya = [k for k in DUMMY_KLAIM if k['email_member'] == email]

    if status_filter != 'semua':
        klaim_filtered = [k for k in klaim_saya if k['status_penerimaan'] == status_filter]
    else:
        klaim_filtered = klaim_saya

    klaim_list = enrich_klaim(klaim_filtered)

    stats = {
        'total':     len(klaim_saya),
        'menunggu':  len([k for k in klaim_saya if k['status_penerimaan'] == 'Menunggu']),
        'disetujui': len([k for k in klaim_saya if k['status_penerimaan'] == 'Disetujui']),
        'ditolak':   len([k for k in klaim_saya if k['status_penerimaan'] == 'Ditolak']),
    }

    context = {
        'role': 'member',
        'klaim_list': klaim_list,
        'status_filter': status_filter,
        'bandara_list': DUMMY_BANDARA,
        'maskapai_list': DUMMY_MASKAPAI,
        'kelas_list': DUMMY_KELAS,
        'stats': stats,
        'success_msg': request.session.pop('success_msg', None),
        'error_msg': request.session.pop('error_msg', None),
    }
    return render(request, 'klaim_member.html', context)


def klaim_ajukan(request):
    """C — Member mengajukan klaim baru."""
    role = request.session.get('role')
    if not role or role != 'member':
        return redirect('login')

    if request.method == 'POST':
        email = request.session.get('email')
        maskapai        = request.POST.get('maskapai', '').strip()
        bandara_asal    = request.POST.get('bandara_asal', '').strip()
        bandara_tujuan  = request.POST.get('bandara_tujuan', '').strip()
        tgl_penerbangan = request.POST.get('tanggal_penerbangan', '').strip()
        flight_number   = request.POST.get('flight_number', '').strip()
        nomor_tiket     = request.POST.get('nomor_tiket', '').strip()
        kelas_kabin     = request.POST.get('kelas_kabin', '').strip()
        pnr             = request.POST.get('pnr', '').strip()

        # Validasi field kosong
        if not all([maskapai, bandara_asal, bandara_tujuan,
                    tgl_penerbangan, flight_number, nomor_tiket, kelas_kabin, pnr]):
            request.session['error_msg'] = 'Semua field wajib diisi.'
            return redirect('klaim_member')

        # Bandara asal ≠ tujuan
        if bandara_asal == bandara_tujuan:
            request.session['error_msg'] = 'Bandara asal dan tujuan tidak boleh sama.'
            return redirect('klaim_member')

        # Cek duplikat
        for k in DUMMY_KLAIM:
            if (k['email_member'] == email
                    and k['flight_number'] == flight_number
                    and k['tanggal_penerbangan'] == tgl_penerbangan
                    and k['nomor_tiket'] == nomor_tiket):
                request.session['error_msg'] = (
                    f'Klaim duplikat! Penerbangan {flight_number} pada '
                    f'{tgl_penerbangan} dengan tiket {nomor_tiket} sudah pernah diklaim.'
                )
                return redirect('klaim_member')

        new_id = next_klaim_id()
        DUMMY_KLAIM.append({
            'id': new_id,
            'email_member': email,
            'nomor_klaim': f'CLM-{new_id:03d}',
            'maskapai': maskapai,
            'nama_maskapai': get_nama_maskapai(maskapai),
            'bandara_asal': bandara_asal,
            'bandara_tujuan': bandara_tujuan,
            'tanggal_penerbangan': tgl_penerbangan,
            'flight_number': flight_number,
            'nomor_tiket': nomor_tiket,
            'kelas_kabin': kelas_kabin,
            'pnr': pnr,
            'status_penerimaan': 'Menunggu',
            'timestamp': '2026-04-30 10:00:00',
            'email_staf': None,
        })
        request.session['success_msg'] = f'Klaim CLM-{new_id:03d} berhasil diajukan!'

    return redirect('klaim_member')


def klaim_edit(request, klaim_id):
    """U — Member mengedit klaim berstatus Menunggu."""
    role = request.session.get('role')
    if not role or role != 'member':
        return redirect('login')

    email = request.session.get('email')
    klaim = next((k for k in DUMMY_KLAIM if k['id'] == klaim_id), None)

    if not klaim or klaim['email_member'] != email:
        request.session['error_msg'] = 'Klaim tidak ditemukan.'
        return redirect('klaim_member')

    if klaim['status_penerimaan'] != 'Menunggu':
        request.session['error_msg'] = 'Hanya klaim berstatus Menunggu yang dapat diedit.'
        return redirect('klaim_member')

    if request.method == 'POST':
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

        # Cek duplikat (kecuali klaim ini sendiri)
        for k in DUMMY_KLAIM:
            if (k['id'] != klaim_id
                    and k['email_member'] == email
                    and k['flight_number'] == flight_number
                    and k['tanggal_penerbangan'] == tgl_penerbangan
                    and k['nomor_tiket'] == nomor_tiket):
                request.session['error_msg'] = 'Klaim duplikat terdeteksi.'
                return redirect('klaim_member')

        klaim.update({
            'maskapai': maskapai,
            'nama_maskapai': get_nama_maskapai(maskapai),
            'bandara_asal': bandara_asal,
            'bandara_tujuan': bandara_tujuan,
            'tanggal_penerbangan': tgl_penerbangan,
            'flight_number': flight_number,
            'nomor_tiket': nomor_tiket,
            'kelas_kabin': kelas_kabin,
            'pnr': pnr,
        })
        request.session['success_msg'] = f'Klaim {klaim["nomor_klaim"]} berhasil diperbarui.'

    return redirect('klaim_member')


def klaim_batalkan(request, klaim_id):
    """D — Member membatalkan klaim berstatus Menunggu."""
    role = request.session.get('role')
    if not role or role != 'member':
        return redirect('login')

    email = request.session.get('email')
    klaim = next((k for k in DUMMY_KLAIM if k['id'] == klaim_id), None)

    if not klaim or klaim['email_member'] != email:
        request.session['error_msg'] = 'Klaim tidak ditemukan.'
        return redirect('klaim_member')

    if klaim['status_penerimaan'] != 'Menunggu':
        request.session['error_msg'] = 'Hanya klaim berstatus Menunggu yang dapat dibatalkan.'
        return redirect('klaim_member')

    if request.method == 'POST':
        nomor = klaim['nomor_klaim']
        DUMMY_KLAIM.remove(klaim)
        request.session['success_msg'] = f'Klaim {nomor} berhasil dibatalkan.'

    return redirect('klaim_member')


# ─── FITUR 9: KLAIM MISSING MILES – STAF (RU) ────────────────────────────────

def klaim_staf(request):
    """R — Staf melihat seluruh klaim dari semua member."""
    role = request.session.get('role')
    if not role or role != 'staf':
        return redirect('login')

    status_filter   = request.GET.get('status', 'semua')
    maskapai_filter = request.GET.get('maskapai', 'semua')
    tgl_dari        = request.GET.get('tgl_dari', '')
    tgl_sampai      = request.GET.get('tgl_sampai', '')
    search          = request.GET.get('search', '').lower()

    filtered = list(DUMMY_KLAIM)

    if status_filter != 'semua':
        filtered = [k for k in filtered if k['status_penerimaan'] == status_filter]
    if maskapai_filter != 'semua':
        filtered = [k for k in filtered if k['maskapai'] == maskapai_filter]
    if tgl_dari:
        filtered = [k for k in filtered if k['timestamp'][:10] >= tgl_dari]
    if tgl_sampai:
        filtered = [k for k in filtered if k['timestamp'][:10] <= tgl_sampai]
    if search:
        filtered = [k for k in filtered if search in k['email_member'].lower()]

    klaim_list = enrich_klaim(filtered)

    email_staf = request.session.get('email')
    stats = {
        'total_menunggu':  len([k for k in DUMMY_KLAIM if k['status_penerimaan'] == 'Menunggu']),
        'disetujui_saya':  len([k for k in DUMMY_KLAIM
                                if k['status_penerimaan'] == 'Disetujui'
                                and k['email_staf'] == email_staf]),
        'ditolak_saya':    len([k for k in DUMMY_KLAIM
                                if k['status_penerimaan'] == 'Ditolak'
                                and k['email_staf'] == email_staf]),
    }

    context = {
        'role': 'staf',
        'klaim_list': klaim_list,
        'maskapai_list': DUMMY_MASKAPAI,
        'stats': stats,
        'status_filter': status_filter,
        'maskapai_filter': maskapai_filter,
        'tgl_dari': tgl_dari,
        'tgl_sampai': tgl_sampai,
        'search': search,
        'success_msg': request.session.pop('success_msg', None),
        'error_msg': request.session.pop('error_msg', None),
    }
    return render(request, 'klaim_staf.html', context)


def klaim_proses(request, klaim_id):
    """U — Staf menyetujui atau menolak klaim."""
    role = request.session.get('role')
    if not role or role != 'staf':
        return redirect('login')

    klaim = next((k for k in DUMMY_KLAIM if k['id'] == klaim_id), None)

    if not klaim:
        request.session['error_msg'] = 'Klaim tidak ditemukan.'
        return redirect('klaim_staf')

    if klaim['status_penerimaan'] != 'Menunggu':
        request.session['error_msg'] = 'Klaim ini sudah diproses sebelumnya.'
        return redirect('klaim_staf')

    if request.method == 'POST':
        aksi = request.POST.get('aksi', '')
        email_staf = request.session.get('email')

        if aksi == 'setujui':
            klaim['status_penerimaan'] = 'Disetujui'
            klaim['email_staf'] = email_staf
            request.session['success_msg'] = (
                f'Klaim {klaim["nomor_klaim"]} DISETUJUI. '
                f'Miles akan ditambahkan ke akun member.'
            )
        elif aksi == 'tolak':
            klaim['status_penerimaan'] = 'Ditolak'
            klaim['email_staf'] = email_staf
            request.session['success_msg'] = f'Klaim {klaim["nomor_klaim"]} DITOLAK.'
        else:
            request.session['error_msg'] = 'Aksi tidak valid.'

    return redirect('klaim_staf')

# ─── TAMBAHKAN KE views.py (di bagian bawah) ─────────────────────────────────

# ─── DUMMY DATA TAMBAHAN ─────────────────────────────────────────────────────

DUMMY_PAKET = [
    {'id': 'AMP-001', 'harga_paket': 150000,  'jumlah_award_miles': 1000},
    {'id': 'AMP-002', 'harga_paket': 650000,  'jumlah_award_miles': 5000},
    {'id': 'AMP-003', 'harga_paket': 1200000, 'jumlah_award_miles': 10000},
    {'id': 'AMP-004', 'harga_paket': 2750000, 'jumlah_award_miles': 25000},
    {'id': 'AMP-005', 'harga_paket': 5000000, 'jumlah_award_miles': 50000},
]

DUMMY_HADIAH = [
    {'kode_hadiah': 'RWD-001', 'nama': 'Upgrade Business Class',   'miles': 15000, 'deskripsi': 'Upgrade kursi ke Business Class.',        'program_end': '2026-12-31'},
    {'kode_hadiah': 'RWD-002', 'nama': 'Extra Baggage 20kg',       'miles': 8000,  'deskripsi': 'Tambahan bagasi sebesar 20kg.',           'program_end': '2026-12-31'},
    {'kode_hadiah': 'RWD-003', 'nama': 'Airport Lounge Access',    'miles': 12000, 'deskripsi': 'Akses lounge bandara internasional.',     'program_end': '2026-12-31'},
    {'kode_hadiah': 'RWD-004', 'nama': 'Hotel Voucher Rp500.000',  'miles': 10000, 'deskripsi': 'Voucher menginap di Hotel Plus.',         'program_end': '2026-12-31'},
    {'kode_hadiah': 'RWD-005', 'nama': 'Travel Voucher Rp300.000', 'miles': 7000,  'deskripsi': 'Voucher pembelian tiket di Travel Mart.', 'program_end': '2026-12-31'},
    {'kode_hadiah': 'RWD-006', 'nama': 'Dining Voucher Rp250.000', 'miles': 6000,  'deskripsi': 'Voucher makan di merchant Foodies.',      'program_end': '2026-12-31'},
    {'kode_hadiah': 'RWD-007', 'nama': 'Shopping Voucher Rp400.000','miles': 9000, 'deskripsi': 'Voucher belanja di ShopIndo.',            'program_end': '2026-12-31'},
    {'kode_hadiah': 'RWD-008', 'nama': 'Car Rental Discount',      'miles': 11000, 'deskripsi': 'Diskon sewa mobil dari RentCar Nusantara.','program_end': '2026-12-31'},
    {'kode_hadiah': 'RWD-009', 'nama': 'Priority Boarding',        'miles': 5000,  'deskripsi': 'Fasilitas naik pesawat lebih awal.',      'program_end': '2026-12-31'},
    {'kode_hadiah': 'RWD-010', 'nama': 'Free Seat Selection',      'miles': 4000,  'deskripsi': 'Bebas memilih kursi penerbangan.',        'program_end': '2026-12-31'},
]

# In-memory storage untuk simulasi transaksi
DUMMY_TRANSFER = []
DUMMY_REDEEM   = []
DUMMY_BELI     = []


# ─── FITUR: TRANSFER MILES ────────────────────────────────────────────────────

def transfer_miles(request):
    role = request.session.get('role')
    if not role or role != 'member':
        return redirect('login')

    email = request.session.get('email')

    riwayat = []
    for t in DUMMY_TRANSFER:
        if t['email_dari'] == email:
            riwayat.append({**t, 'tipe': 'keluar', 'email_lain': t['email_ke']})
        elif t['email_ke'] == email:
            riwayat.append({**t, 'tipe': 'masuk', 'email_lain': t['email_dari']})
    riwayat.sort(key=lambda x: x['timestamp'], reverse=True)

    total_keluar = sum(t['jumlah'] for t in riwayat if t['tipe'] == 'keluar')
    total_masuk  = sum(t['jumlah'] for t in riwayat if t['tipe'] == 'masuk')

    context = {
        'role': 'member',
        'total_miles': '45,000',
        'riwayat': riwayat,
        'stats': {
            'total_keluar': total_keluar,
            'total_masuk':  total_masuk,
        },
        'success_msg': request.session.pop('success_msg', None),
        'error_msg':   request.session.pop('error_msg', None),
    }
    return render(request, 'transfer.html', context)


def transfer_kirim(request):
    role = request.session.get('role')
    if not role or role != 'member':
        return redirect('login')

    if request.method == 'POST':
        email_dari    = request.session.get('email')
        email_tujuan  = request.POST.get('email_tujuan', '').strip()
        jumlah_str    = request.POST.get('jumlah', '').strip()
        catatan       = request.POST.get('catatan', '').strip()

        if not email_tujuan or not jumlah_str:
            request.session['error_msg'] = 'Email tujuan dan jumlah wajib diisi.'
            return redirect('transfer_miles')

        if email_tujuan == email_dari:
            request.session['error_msg'] = 'Tidak dapat transfer ke diri sendiri.'
            return redirect('transfer_miles')

        try:
            jumlah = int(jumlah_str)
            if jumlah < 100:
                raise ValueError
        except ValueError:
            request.session['error_msg'] = 'Jumlah miles minimal 100.'
            return redirect('transfer_miles')

        DUMMY_TRANSFER.append({
            'email_dari':  email_dari,
            'email_ke':    email_tujuan,
            'jumlah':      jumlah,
            'catatan':     catatan,
            'timestamp':   '2026-04-30 10:00:00',
        })
        request.session['success_msg'] = f'{jumlah} miles berhasil dikirim ke {email_tujuan}.'

    return redirect('transfer_miles')


# ─── FITUR: REDEEM HADIAH ─────────────────────────────────────────────────────

def redeem_hadiah(request):
    role = request.session.get('role')
    if not role or role != 'member':
        return redirect('login')

    email = request.session.get('email')
    riwayat_redeem = []
    for r in DUMMY_REDEEM:
        if r['email_member'] == email:
            hadiah = next((h for h in DUMMY_HADIAH if h['kode_hadiah'] == r['kode_hadiah']), {})
            riwayat_redeem.append({
                **r,
                'nama_hadiah': hadiah.get('nama', '-'),
                'miles':       hadiah.get('miles', 0),
            })
    riwayat_redeem.sort(key=lambda x: x['timestamp'], reverse=True)

    miles_digunakan = sum(r['miles'] for r in riwayat_redeem)

    context = {
        'role': 'member',
        'award_miles': 32000,
        'hadiah_list': DUMMY_HADIAH,
        'riwayat_redeem': riwayat_redeem,
        'stats': {
            'total_redeem':    len(riwayat_redeem),
            'miles_digunakan': miles_digunakan,
        },
        'success_msg': request.session.pop('success_msg', None),
        'error_msg':   request.session.pop('error_msg', None),
    }
    return render(request, 'redeem.html', context)


def redeem_proses(request):
    role = request.session.get('role')
    if not role or role != 'member':
        return redirect('login')

    if request.method == 'POST':
        email       = request.session.get('email')
        kode_hadiah = request.POST.get('kode_hadiah', '').strip()

        hadiah = next((h for h in DUMMY_HADIAH if h['kode_hadiah'] == kode_hadiah), None)
        if not hadiah:
            request.session['error_msg'] = 'Hadiah tidak ditemukan.'
            return redirect('redeem_hadiah')

        DUMMY_REDEEM.append({
            'email_member': email,
            'kode_hadiah':  kode_hadiah,
            'timestamp':    '2026-04-30 10:00:00',
        })
        request.session['success_msg'] = f'Redeem "{hadiah["nama"]}" berhasil! {hadiah["miles"]} miles dikurangi.'

    return redirect('redeem_hadiah')


# ─── FITUR: BELI PACKAGE ─────────────────────────────────────────────────────

def beli_package(request):
    role = request.session.get('role')
    if not role or role != 'member':
        return redirect('login')

    email = request.session.get('email')
    riwayat_beli = [b for b in DUMMY_BELI if b['email_member'] == email]
    riwayat_beli.sort(key=lambda x: x['timestamp'], reverse=True)

    miles_dibeli  = sum(b['jumlah_miles'] for b in riwayat_beli)

    riwayat_display = []
    for b in riwayat_beli:
        paket = next((p for p in DUMMY_PAKET if p['id'] == b['id_paket']), {})
        riwayat_display.append({
            **b,
            'harga': paket.get('harga_paket', 0),
        })

    context = {
        'role': 'member',
        'award_miles': 32000,
        'paket_list':  DUMMY_PAKET,
        'riwayat_beli': riwayat_display,
        'stats': {
            'total_beli':  len(riwayat_beli),
            'miles_dibeli': miles_dibeli,
        },
        'success_msg': request.session.pop('success_msg', None),
        'error_msg':   request.session.pop('error_msg', None),
    }
    return render(request, 'package.html', context)


def package_beli(request):
    role = request.session.get('role')
    if not role or role != 'member':
        return redirect('login')

    if request.method == 'POST':
        email    = request.session.get('email')
        id_paket = request.POST.get('id_paket', '').strip()

        paket = next((p for p in DUMMY_PAKET if p['id'] == id_paket), None)
        if not paket:
            request.session['error_msg'] = 'Paket tidak ditemukan.'
            return redirect('beli_package')

        DUMMY_BELI.append({
            'email_member': email,
            'id_paket':     id_paket,
            'jumlah_miles': paket['jumlah_award_miles'],
            'timestamp':    '2026-04-30 10:00:00',
        })
        request.session['success_msg'] = (
            f'Pembelian {id_paket} berhasil! '
            f'{paket["jumlah_award_miles"]} award miles ditambahkan.'
        )

    return redirect('beli_package')

from django.shortcuts import render, redirect
from datetime import datetime, date

DUMMY_PENYEDIA = [
    {'id': '1', 'nama': 'Hotel Plus Indonesia', 'tipe': 'partner'},
    {'id': '2', 'nama': 'Garuda Indonesia', 'tipe': 'airline'},
]

DUMMY_HADIAH = []

def cek_status_aktif(start, end):
    today = date.today()
    start = datetime.strptime(start, "%Y-%m-%d").date()
    end = datetime.strptime(end, "%Y-%m-%d").date()
    return start <= today <= end

def get_penyedia_info(id_penyedia):
    for p in DUMMY_PENYEDIA:
        if p['id'] == id_penyedia:
            return p['nama'], p['tipe']
    return '-', '-'

from django.shortcuts import render, redirect
from django.contrib import messages

# helper ambil data dari session
def get_hadiah_session(request):
    return request.session.get('hadiah_list', [])

def save_hadiah_session(request, data):
    request.session['hadiah_list'] = data

from django.shortcuts import render, redirect
from django.contrib import messages

# helper ambil data dari session
def get_hadiah_session(request):
    return request.session.get('hadiah_list', [])

def save_hadiah_session(request, data):
    request.session['hadiah_list'] = data

def kelola_hadiah(request):
    hadiah_list = get_hadiah_session(request)

    penyedia_filter = request.GET.get('penyedia', 'semua')
    status_filter = request.GET.get('status', 'semua')
    search = request.GET.get('search', '')

    if penyedia_filter != 'semua':
        hadiah_list = [h for h in hadiah_list if h['id_penyedia'] == penyedia_filter]

    if status_filter == 'aktif':
        hadiah_list = [h for h in hadiah_list if h['is_active']]
    elif status_filter == 'expired':
        hadiah_list = [h for h in hadiah_list if not h['is_active']]

    if search:
        hadiah_list = [h for h in hadiah_list if search.lower() in h['nama'].lower()]

    stats = {
        'total': len(get_hadiah_session(request)),
        'aktif': len([h for h in get_hadiah_session(request) if h['is_active']]),
        'expired': len([h for h in get_hadiah_session(request) if not h['is_active']]),
        'penyedia': len(DUMMY_PENYEDIA),
    }

    return render(request, 'kelola_hadiah.html', {
        'hadiah_list': hadiah_list,
        'penyedia_list': DUMMY_PENYEDIA,
        'penyedia_filter': penyedia_filter,
        'status_filter': status_filter,
        'search': search,
        'stats': stats,
    })

def hadiah_tambah(request):
    if request.method == 'POST':
        hadiah_list = get_hadiah_session(request)

        kode = f"RWD-{len(hadiah_list)+1:03d}"

        nama = request.POST.get('nama')
        deskripsi = request.POST.get('deskripsi')
        id_penyedia = request.POST.get('id_penyedia')
        miles = int(request.POST.get('miles'))
        start = request.POST.get('valid_start_date')
        end = request.POST.get('program_end')

        nama_penyedia, tipe = get_penyedia_info(id_penyedia)

        hadiah_list.append({
            'kode_hadiah': kode,
            'nama': nama,
            'deskripsi': deskripsi,
            'id_penyedia': id_penyedia,
            'nama_penyedia': nama_penyedia,
            'tipe_penyedia': tipe,
            'miles': miles,
            'valid_start_date': start,
            'program_end': end,
            'is_active': cek_status_aktif(start, end)
        })

        save_hadiah_session(request, hadiah_list)

    return redirect('kelola_hadiah')

def edit_hadiah(request, kode):
    if request.method == 'POST':
        hadiah_list = get_hadiah_session(request)

        for h in hadiah_list:
            if h['kode_hadiah'] == kode:
                h['nama'] = request.POST.get('nama')
                h['deskripsi'] = request.POST.get('deskripsi')
                h['id_penyedia'] = request.POST.get('id_penyedia')
                h['miles'] = int(request.POST.get('miles'))
                h['valid_start_date'] = request.POST.get('valid_start_date')
                h['program_end'] = request.POST.get('program_end')

                nama_penyedia, tipe = get_penyedia_info(h['id_penyedia'])
                h['nama_penyedia'] = nama_penyedia
                h['tipe_penyedia'] = tipe

                h['is_active'] = cek_status_aktif(
                    h['valid_start_date'],
                    h['program_end']
                )
                break

        save_hadiah_session(request, hadiah_list)

    return redirect('kelola_hadiah')

def hapus_hadiah(request, kode):
    if request.method == 'POST':
        hadiah_list = get_hadiah_session(request)

        new_list = []
        found = False

        for h in hadiah_list:
            if h['kode_hadiah'] == kode:
                found = True

                if h['is_active']:
                    messages.error(request, "Hadiah aktif tidak bisa dihapus.")
                    return redirect('kelola_hadiah')

                continue  # skip = delete
            new_list.append(h)

        if not found:
            messages.error(request, "Hadiah tidak ditemukan.")
        else:
            save_hadiah_session(request, new_list)
            messages.success(request, "Hadiah berhasil dihapus.")

    return redirect('kelola_hadiah')

from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import date

# ===== DUMMY =====
DUMMY_MITRA = [
    {
        "email_mitra": "hotelplus@aeromiles.id",
        "nama_mitra": "Hotel Plus Indonesia",
        "tanggal_kerja_sama": "2023-01-15",
        "id_penyedia": "4"
    },
    {
        "email_mitra": "travelmart@aeromiles.id",
        "nama_mitra": "Travel Mart Asia",
        "tanggal_kerja_sama": "2023-03-20",
        "id_penyedia": "5"
    },
]

# ═══════════════════════════════════════════════════════════
# TAMBAHKAN KE views.py — bagian DUMMY DATA (atas file)
# ═══════════════════════════════════════════════════════════

DUMMY_MITRA = [
    {
        'id_penyedia': 4,
        'email_mitra': 'partner@traveloka.com',
        'nama_mitra': 'TravelokaPartner',
        'tanggal_kerja_sama': '2023-01-15',
    },
    {
        'id_penyedia': 5,
        'email_mitra': 'partner@plazapremium.com',
        'nama_mitra': 'Plaza Premium',
        'tanggal_kerja_sama': '2023-06-01',
    },
    {
        'id_penyedia': 6,
        'email_mitra': 'partner@foodies.com',
        'nama_mitra': 'Foodies Reward',
        'tanggal_kerja_sama': '2024-01-10',
    },
    {
        'id_penyedia': 7,
        'email_mitra': 'partner@shopindo.com',
        'nama_mitra': 'ShopIndo Voucher',
        'tanggal_kerja_sama': '2024-03-20',
    },
    {
        'id_penyedia': 8,
        'email_mitra': 'partner@rentcar.com',
        'nama_mitra': 'RentCar Nusantara',
        'tanggal_kerja_sama': '2024-06-05',
    },
]

def _next_penyedia_id():
    """Auto-increment ID penyedia."""
    if not DUMMY_MITRA:
        return 10
    return max(m['id_penyedia'] for m in DUMMY_MITRA) + 1


# ═══════════════════════════════════════════════════════════
# TAMBAHKAN KE views.py — bagian VIEWS (bawah file)
# ═══════════════════════════════════════════════════════════

def kelola_mitra(request):
    """R — Staf melihat daftar mitra."""
    role = request.session.get('role')
    if not role or role != 'staf':
        return redirect('login')

    search = request.GET.get('search', '').lower()

    filtered = list(DUMMY_MITRA)
    if search:
        filtered = [
            m for m in filtered
            if search in m['nama_mitra'].lower()
            or search in m['email_mitra'].lower()
        ]

    # Hitung hadiah yang dimiliki mitra (dari DUMMY_HADIAH di views.py)
    # Karena dummy, kita pakai angka statis. Ganti dengan lookup nyata jika sudah ada.
    stats = {
        'total':  len(DUMMY_MITRA),
        'aktif':  len(DUMMY_MITRA),  # semua aktif untuk dummy
        'hadiah': sum(
            1 for h in DUMMY_HADIAH
            if any(m['id_penyedia'] == h.get('id_penyedia') for m in DUMMY_MITRA)
        ) if 'DUMMY_HADIAH' in dir() else 0,
    }

    context = {
        'role':       'staf',
        'mitra_list': filtered,
        'search':     search,
        'stats':      stats,
        'success_msg': request.session.pop('success_msg', None),
        'error_msg':   request.session.pop('error_msg', None),
    }
    return render(request, 'kelola_mitra.html', context)


def mitra_tambah(request):
    """C — Staf menambahkan mitra baru + otomatis buat entri PENYEDIA."""
    role = request.session.get('role')
    if not role or role != 'staf':
        return redirect('login')

    if request.method == 'POST':
        email_mitra        = request.POST.get('email_mitra', '').strip()
        nama_mitra         = request.POST.get('nama_mitra', '').strip()
        tanggal_kerja_sama = request.POST.get('tanggal_kerja_sama', '').strip()

        # Validasi field kosong
        if not all([email_mitra, nama_mitra, tanggal_kerja_sama]):
            request.session['error_msg'] = 'Semua field wajib diisi.'
            return redirect('kelola_mitra')

        # Cek email duplikat (email mitra adalah PK)
        if any(m['email_mitra'] == email_mitra for m in DUMMY_MITRA):
            request.session['error_msg'] = f'Email {email_mitra} sudah terdaftar sebagai mitra.'
            return redirect('kelola_mitra')

        # Auto-generate id_penyedia baru
        new_id = _next_penyedia_id()

        DUMMY_MITRA.append({
            'id_penyedia':        new_id,
            'email_mitra':        email_mitra,
            'nama_mitra':         nama_mitra,
            'tanggal_kerja_sama': tanggal_kerja_sama,
        })
        request.session['success_msg'] = f'Mitra "{nama_mitra}" berhasil ditambahkan (ID Penyedia: P-{new_id}).'

    return redirect('kelola_mitra')


def mitra_edit(request, email_mitra):
    """U — Staf memperbarui nama dan tanggal kerja sama mitra.
       Email mitra (PK) dan ID Penyedia TIDAK bisa diubah sesuai soal.
    """
    role = request.session.get('role')
    if not role or role != 'staf':
        return redirect('login')

    mitra = next((m for m in DUMMY_MITRA if m['email_mitra'] == email_mitra), None)

    if not mitra:
        request.session['error_msg'] = 'Mitra tidak ditemukan.'
        return redirect('kelola_mitra')

    if request.method == 'POST':
        nama_baru  = request.POST.get('nama_mitra', '').strip()
        tgl_baru   = request.POST.get('tanggal_kerja_sama', '').strip()

        if not nama_baru or not tgl_baru:
            request.session['error_msg'] = 'Nama dan tanggal wajib diisi.'
            return redirect('kelola_mitra')

        mitra['nama_mitra']         = nama_baru
        mitra['tanggal_kerja_sama'] = tgl_baru

        request.session['success_msg'] = f'Mitra "{nama_baru}" berhasil diperbarui.'

    return redirect('kelola_mitra')


def mitra_hapus(request, email_mitra):
    """D — Staf menghapus mitra. Penghapusan juga menghapus hadiah terkait."""
    role = request.session.get('role')
    if not role or role != 'staf':
        return redirect('login')

    mitra = next((m for m in DUMMY_MITRA if m['email_mitra'] == email_mitra), None)

    if not mitra:
        request.session['error_msg'] = 'Mitra tidak ditemukan.'
        return redirect('kelola_mitra')

    if request.method == 'POST':
        nama = mitra['nama_mitra']
        id_p = mitra['id_penyedia']

        # Hapus hadiah terkait (ON DELETE CASCADE sesuai skema)
        # Jika DUMMY_HADIAH ada di scope, hapus hadiah dengan id_penyedia yang sama
        try:
            hadiah_terhapus = [h for h in DUMMY_HADIAH if h.get('id_penyedia') == id_p]
            for h in hadiah_terhapus:
                DUMMY_HADIAH.remove(h)
            cascade_info = f' ({len(hadiah_terhapus)} hadiah ikut dihapus)' if hadiah_terhapus else ''
        except NameError:
            cascade_info = ''

        DUMMY_MITRA.remove(mitra)
        request.session['success_msg'] = f'Mitra "{nama}" berhasil dihapus{cascade_info}.'

    return redirect('kelola_mitra')

# laporan
# ═══════════════════════════════════════════════════════════════════════════════
# TAMBAHAN views.py — LAPORAN TRANSAKSI
# Tempel ke bagian DUMMY DATA (atas) dan VIEWS (bawah) di views.py yang sudah ada
# ═══════════════════════════════════════════════════════════════════════════════

# ─── DUMMY DATA TAMBAHAN ──────────────────────────────────────────────────────
# Letakkan bersama DUMMY_KLAIM, DUMMY_MEMBER_INFO, dll. di atas file

DUMMY_TRANSFER = [
    {
        'email_member_1': 'john@example.com',
        'email_member_2': 'siti.nurhaliza@email.com',
        'jumlah': 5000,
        'catatan': 'Transfer untuk liburan bersama',
        'timestamp': '2024-10-10 09:00:00',
    },
    {
        'email_member_1': 'eka.putra@email.com',
        'email_member_2': 'john@example.com',
        'jumlah': 3500,
        'catatan': None,
        'timestamp': '2024-11-05 14:30:00',
    },
    {
        'email_member_1': 'budi.santoso@email.com',
        'email_member_2': 'dewi.lestari@email.com',
        'jumlah': 10000,
        'catatan': 'Hadiah ulang tahun',
        'timestamp': '2024-12-20 18:00:00',
    },
    {
        'email_member_1': 'siti.nurhaliza@email.com',
        'email_member_2': 'budi.santoso@email.com',
        'jumlah': 2500,
        'catatan': None,
        'timestamp': '2025-01-08 11:15:00',
    },
    {
        'email_member_1': 'dewi.lestari@email.com',
        'email_member_2': 'eka.putra@email.com',
        'jumlah': 7500,
        'catatan': 'Bagi-bagi miles',
        'timestamp': '2025-02-14 20:00:00',
    },
]

DUMMY_REDEEM = [
    {
        'email_member': 'john@example.com',
        'kode_hadiah': 'HDH-001',
        'nama_hadiah': 'Upgrade Business Class',
        'miles': 25000,
        'timestamp': '2024-10-15 10:00:00',
    },
    {
        'email_member': 'siti.nurhaliza@email.com',
        'kode_hadiah': 'HDH-002',
        'nama_hadiah': 'Voucher Hotel Premium',
        'miles': 15000,
        'timestamp': '2024-11-22 13:45:00',
    },
    {
        'email_member': 'eka.putra@email.com',
        'kode_hadiah': 'HDH-001',
        'nama_hadiah': 'Upgrade Business Class',
        'miles': 25000,
        'timestamp': '2025-01-20 09:30:00',
    },
    {
        'email_member': 'budi.santoso@email.com',
        'kode_hadiah': 'HDH-003',
        'nama_hadiah': 'Voucher Makan Foodies',
        'miles': 8000,
        'timestamp': '2025-02-05 17:00:00',
    },
    {
        'email_member': 'dewi.lestari@email.com',
        'kode_hadiah': 'HDH-004',
        'nama_hadiah': 'Voucher Belanja ShopIndo',
        'miles': 14000,
        'timestamp': '2025-03-10 12:00:00',
    },
]

DUMMY_BELI_PACKAGE = [
    {
        'email_member': 'john@example.com',
        'id_award_miles_package': 'AMP-001',
        'jumlah_miles': 50000,
        'harga': '2,500,000',
        'timestamp': '2024-09-01 08:00:00',
    },
    {
        'email_member': 'siti.nurhaliza@email.com',
        'id_award_miles_package': 'AMP-002',
        'jumlah_miles': 100000,
        'harga': '4,500,000',
        'timestamp': '2024-10-10 09:30:00',
    },
    {
        'email_member': 'eka.putra@email.com',
        'id_award_miles_package': 'AMP-003',
        'jumlah_miles': 200000,
        'harga': '8,000,000',
        'timestamp': '2024-12-05 15:00:00',
    },
    {
        'email_member': 'budi.santoso@email.com',
        'id_award_miles_package': 'AMP-001',
        'jumlah_miles': 50000,
        'harga': '2,500,000',
        'timestamp': '2025-01-18 11:00:00',
    },
    {
        'email_member': 'dewi.lestari@email.com',
        'id_award_miles_package': 'AMP-003',
        'jumlah_miles': 200000,
        'harga': '8,000,000',
        'timestamp': '2025-03-01 10:15:00',
    },
]

# ─── DUMMY BAR CHART DATA ─────────────────────────────────────────────────────
# Volume transaksi per bulan (semua jenis digabung) — untuk chart di template

DUMMY_BAR_DATA_RAW = [
    ('Jan', 42), ('Feb', 58), ('Mar', 33), ('Apr', 71),
    ('Mei', 52), ('Jun', 85), ('Jul', 64), ('Agu', 90),
    ('Sep', 47), ('Okt', 73), ('Nov', 60), ('Des', 95),
]

COLORS_BAR = [
    'rgba(96,165,250,0.7)',  'rgba(167,139,250,0.6)', 'rgba(96,165,250,0.6)',
    'rgba(251,191,36,0.6)',  'rgba(52,211,153,0.6)',  'rgba(96,165,250,0.8)',
    'rgba(167,139,250,0.6)', 'rgba(52,211,153,0.7)',  'rgba(251,191,36,0.6)',
    'rgba(96,165,250,0.7)',  'rgba(167,139,250,0.6)', 'rgba(52,211,153,0.8)',
]


# ─── VIEW ─────────────────────────────────────────────────────────────────────
# Letakkan bersama view-view lain di bagian bawah file

def laporan_transaksi(request):
    """Halaman laporan transaksi — hanya bisa diakses staf."""
    role = request.session.get('role')
    if not role:
        return redirect('login')
    if role != 'staf':
        return redirect('dashboard')

    # ── Filter params ──────────────────────────────────────────────────────────
    search     = request.GET.get('search', '').strip().lower()
    tgl_dari   = request.GET.get('tgl_dari', '').strip()    # format: YYYY-MM-DD
    tgl_sampai = request.GET.get('tgl_sampai', '').strip()
    active_tab = request.GET.get('tab', 'klaim')

    # ── Helper: filter berdasarkan search + tanggal ────────────────────────────
    def filter_by_date(item, field='timestamp'):
        ts = item.get(field, '')[:10]   # ambil bagian tanggal saja (YYYY-MM-DD)
        if tgl_dari   and ts < tgl_dari:   return False
        if tgl_sampai and ts > tgl_sampai: return False
        return True

    def member_match(email):
        if not search:
            return True
        info = DUMMY_MEMBER_INFO.get(email, {})
        nama = info.get('nama', '').lower()
        return search in email.lower() or search in nama

    # ── Filter KLAIM ───────────────────────────────────────────────────────────
    klaim_filtered = [
        k for k in DUMMY_KLAIM
        if member_match(k['email_member']) and filter_by_date(k)
    ]
    klaim_enriched = enrich_klaim(klaim_filtered)

    # ── Filter TRANSFER ────────────────────────────────────────────────────────
    transfer_filtered = [
        t for t in DUMMY_TRANSFER
        if (member_match(t['email_member_1']) or member_match(t['email_member_2']))
        and filter_by_date(t)
    ]

    # ── Filter REDEEM ──────────────────────────────────────────────────────────
    redeem_filtered = [
        r for r in DUMMY_REDEEM
        if member_match(r['email_member']) and filter_by_date(r)
    ]

    # ── Filter BELI PACKAGE ────────────────────────────────────────────────────
    beli_filtered = [
        b for b in DUMMY_BELI_PACKAGE
        if member_match(b['email_member']) and filter_by_date(b)
    ]

    # ── Stats cards ────────────────────────────────────────────────────────────
    total_miles_klaim    = sum(5000 for k in klaim_enriched if k['status_penerimaan'] == 'Disetujui')   # placeholder
    total_miles_transfer = sum(t['jumlah'] for t in transfer_filtered)
    total_miles_redeem   = sum(r['miles'] for r in redeem_filtered)
    total_miles_dibeli   = sum(b['jumlah_miles'] for b in beli_filtered)

    # Redeem terbanyak
    if redeem_filtered:
        from collections import Counter
        redeem_top = Counter(r['nama_hadiah'] for r in redeem_filtered).most_common(1)[0][0]
    else:
        redeem_top = '—'

    # Paket terlaris
    if beli_filtered:
        from collections import Counter
        paket_top = Counter(b['id_award_miles_package'] for b in beli_filtered).most_common(1)[0][0]
    else:
        paket_top = '—'

    klaim_setuju = sum(1 for k in klaim_enriched if k['status_penerimaan'] == 'Disetujui')

    # Revenue dari pembelian paket (hapus pemisah ribuan lalu jumlahkan)
    try:
        revenue_total = sum(
            int(b['harga'].replace(',', '').replace('.', ''))
            for b in beli_filtered
        )
        revenue_str = f"{revenue_total:,}".replace(',', '.')
    except Exception:
        revenue_str = '0'

    stats = {
        'total_klaim':    len(klaim_enriched),
        'total_transfer': len(transfer_filtered),
        'total_redeem':   len(redeem_filtered),
        'total_beli':     len(beli_filtered),
        'miles_klaim':    f"{total_miles_klaim:,}",
        'miles_transfer': f"{total_miles_transfer:,}",
        'miles_redeem':   f"{total_miles_redeem:,}",
        'miles_dibeli':   f"{total_miles_dibeli:,}",
        'revenue':        revenue_str,
        'redeem_top':     redeem_top,
        'paket_top':      paket_top,
        'klaim_setuju':   f"{klaim_setuju} klaim",
    }

    # ── Bar chart data ─────────────────────────────────────────────────────────
    max_val = max(v for _, v in DUMMY_BAR_DATA_RAW) or 1
    bar_data = [
        {
            'label': label,
            'val':   val,
            'pct':   round(val / max_val * 100),
            'color': COLORS_BAR[i % len(COLORS_BAR)],
        }
        for i, (label, val) in enumerate(DUMMY_BAR_DATA_RAW)
    ]

    context = {
        'role':            'staf',
        'search':          request.GET.get('search', ''),
        'tgl_dari':        tgl_dari,
        'tgl_sampai':      tgl_sampai,
        'active_tab':      active_tab,
        'stats':           stats,
        'bar_data':        bar_data,
        'klaim_list':      klaim_enriched,
        'transfer_list':   transfer_filtered,
        'redeem_list':     redeem_filtered,
        'beli_list':       beli_filtered,
    }
    return render(request, 'laporan_transaksi.html', context)