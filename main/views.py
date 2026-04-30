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


def profil(request):
    role = request.session.get('role')
    if not role:
        return redirect('login')
    return render(request, 'profil.html', {'role': role})


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