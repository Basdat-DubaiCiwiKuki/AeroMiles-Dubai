from django.urls import path
from . import views

urlpatterns = [
    # ── Landing & Auth ────────────────────────────────────────────────────────
    path('',                        views.landing,              name='landing'),
    path('login/',                  views.login_page,           name='login'),
    path('register/',               views.register,             name='register'),
    path('logout/',                 views.logout_view,          name='logout'),

    # ── Dashboard ─────────────────────────────────────────────────────────────
    # Satu view dashboard() menangani member dan staf sekaligus
    path('dashboard/',              views.dashboard,            name='dashboard'),

    # ── Profil ────────────────────────────────────────────────────────────────
    path('profil/',                 views.profil,               name='profil'),
    path('profil/update/',          views.profil_update,        name='profil_update'),
    path('profil/ubah-password/',   views.profil_ubah_password, name='profil_ubah_password'),

    # ── Identitas Member (CRUD) ───────────────────────────────────────────────
    path('identitas/',                          views.identitas,        name='identitas'),
    path('identitas/tambah/',                   views.identitas_tambah, name='identitas_tambah'),
    path('identitas/edit/<str:nomor>/',         views.identitas_edit,   name='identitas_edit'),
    path('identitas/hapus/<str:nomor>/',        views.identitas_hapus,  name='identitas_hapus'),

    # ── Info Tier ─────────────────────────────────────────────────────────────
    path('tier/',                   views.tier,                 name='tier'),

    # ── Klaim Missing Miles — Member (CRUD) ───────────────────────────────────
    path('klaim/',                              views.klaim_member,     name='klaim_member'),
    path('klaim/ajukan/',                       views.klaim_ajukan,     name='klaim_ajukan'),
    path('klaim/edit/<int:klaim_id>/',          views.klaim_edit,       name='klaim_edit'),
    path('klaim/batalkan/<int:klaim_id>/',      views.klaim_batalkan,   name='klaim_batalkan'),

    # ── Klaim Missing Miles — Staf (RU) ───────────────────────────────────────
    path('kelola-klaim/',                               views.klaim_staf,   name='klaim_staf'),
    path('kelola-klaim/proses/<int:klaim_id>/',         views.klaim_proses, name='klaim_proses'),

    # ── Kelola Member — Staf (CRUD) ───────────────────────────────────────────
    path('kelola-member/',                              views.kelola_member,    name='kelola_member'),
    path('kelola-member/tambah/',                       views.member_tambah,    name='member_tambah'),
    path('kelola-member/edit/<str:email_member>/',      views.member_edit,      name='member_edit'),
    path('kelola-member/hapus/<str:email_member>/',     views.member_hapus,     name='member_hapus'),

    # ── Transfer Miles (CR) ───────────────────────────────────────────────────
    path('transfer/',               views.transfer_miles,       name='transfer_miles'),
    path('transfer/kirim/',         views.transfer_kirim,       name='transfer_kirim'),

    # ── Redeem Hadiah (CR) ────────────────────────────────────────────────────
    path('redeem/',                 views.redeem_hadiah,        name='redeem_hadiah'),
    path('redeem/proses/',          views.redeem_proses,        name='redeem_proses'),

    # ── Beli Award Miles Package (CR) ─────────────────────────────────────────
    path('package/',                views.beli_package,         name='beli_package'),
    path('package/beli/',           views.package_beli,         name='package_beli'),

    # ── Kelola Hadiah & Penyedia — Staf (CRUD) ────────────────────────────────
    path('kelola-hadiah/',                          views.kelola_hadiah,    name='kelola_hadiah'),
    path('kelola-hadiah/tambah/',                   views.hadiah_tambah,    name='hadiah_tambah'),
    path('kelola-hadiah/edit/<str:kode>/',          views.hadiah_edit,      name='hadiah_edit'),
    path('kelola-hadiah/hapus/<str:kode>/',         views.hadiah_hapus,     name='hadiah_hapus'),

    # ── Kelola Mitra — Staf (CRUD) ────────────────────────────────────────────
    path('kelola-mitra/',                               views.kelola_mitra,     name='kelola_mitra'),
    path('kelola-mitra/tambah/',                        views.mitra_tambah,     name='mitra_tambah'),
    path('kelola-mitra/edit/<str:email_mitra>/',        views.mitra_edit,       name='mitra_edit'),
    path('kelola-mitra/hapus/<str:email_mitra>/',       views.mitra_hapus,      name='mitra_hapus'),

    # ── Laporan & Riwayat Transaksi — Staf (RD) ──────────────────────────────
    path('laporan-transaksi/',          views.laporan_transaksi,    name='laporan_transaksi'),
    path('laporan-transaksi/hapus/',    views.laporan_hapus,        name='laporan_hapus'),
]