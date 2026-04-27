from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_page, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/staf/', views.dashboard_staf, name='dashboard_staf'),
    path('identitas/', views.identitas, name='identitas'),
    path('register/', views.register, name='register'),
    path('profil/', views.profil, name='profil'),
    path('logout/', views.logout, name='logout'),
]