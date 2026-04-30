from django.urls import path
from . import views

urlpatterns = [
    # Landing & Auth
    path('', views.landing, name='landing'),
    path('login/', views.login_page, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/staf/', views.dashboard_staf, name='dashboard_staf'),

    # Profil & Identitas
    path('profil/',                views.profil,               name='profil'),
    path('profil/update/',         views.profil_update,        name='profil_update'),
    path('profil/ubah-password/',  views.profil_ubah_password, name='profil_ubah_password'),
    path('identitas/', views.identitas, name='identitas'),
    path('tier/', views.tier, name='tier'),

    # Klaim Missing Miles - Member (CRUD)
    path('klaim/', views.klaim_member, name='klaim_member'),
    path('klaim/ajukan/', views.klaim_ajukan, name='klaim_ajukan'),
    path('klaim/edit/<int:klaim_id>/', views.klaim_edit, name='klaim_edit'),
    path('klaim/batalkan/<int:klaim_id>/', views.klaim_batalkan, name='klaim_batalkan'),

    # Klaim Missing Miles - Staf (RU)
    path('kelola-klaim/', views.klaim_staf, name='klaim_staf'),
    path('kelola-klaim/proses/<int:klaim_id>/', views.klaim_proses, name='klaim_proses'),

    # Kelola Member - Staf
    path('kelola-member/', views.kelola_member, name='kelola_member'),

    # Transfer Miles
    path('transfer/', views.transfer_miles, name='transfer_miles'),
    path('transfer/kirim/', views.transfer_kirim, name='transfer_kirim'),

    # Redeem Hadiah
    path('redeem/', views.redeem_hadiah, name='redeem_hadiah'),
    path('redeem/proses/', views.redeem_proses, name='redeem_proses'),

    # Beli Package
    path('package/', views.beli_package, name='beli_package'),
    path('package/beli/', views.package_beli, name='package_beli'),

    # Info Tier (sudah ada, pastikan ada)
    path('tier/', views.tier, name='tier'),

    # Hadiah
    path('kelola-hadiah/', views.kelola_hadiah, name='kelola_hadiah'),
    path('kelola-hadiah/tambah/', views.hadiah_tambah, name='hadiah_tambah'),
    path('kelola-hadiah/edit/<str:kode>/', views.edit_hadiah, name='edit_hadiah'),
    path('kelola-hadiah/hapus/<str:kode>/', views.hapus_hadiah, name='hapus_hadiah'),

    # Mitra
    path('kelola-mitra/',                           views.kelola_mitra,  name='kelola_mitra'),
    path('kelola-mitra/tambah/',                    views.mitra_tambah,  name='mitra_tambah'),
    path('kelola-mitra/edit/<str:email_mitra>/',    views.mitra_edit,    name='mitra_edit'),
    path('kelola-mitra/hapus/<str:email_mitra>/',   views.mitra_hapus,   name='mitra_hapus'),

    path('kelola-member/', views.kelola_member, name='kelola_member'),

    path('laporan-transaksi/', views.laporan_transaksi, name="laporan_transaksi"),
]