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
    path('profil/', views.profil, name='profil'),
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
]