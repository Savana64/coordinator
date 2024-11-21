from django.urls import path
from django.shortcuts import render
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from .views import set_cookie_view

app_name = 'depo'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('buses/', views.bus_list, name='bus_list'),
    path('drivers/', views.driver_list, name='driver_list'),
    path('reservations/', views.reservation_list, name='reservation_list'),
    path('reservations/delete/<int:reservation_id>/', views.delete_reservation, name='delete_reservation'),
    path('reservation/update/<int:reservation_id>/', views.update_reservation, name='update_reservation'),
    path('add_reservation/', views.add_reservation, name='add_reservation'),
    path('login/', auth_views.LoginView.as_view(template_name='depo/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view( template_name='depo/logout.html'), name='logout'),
    path('privacy_policy/', lambda request: render(request,'depo/privacy_policy.html'), name='privacy_policy'),
    path('register/', views.register, name='register'),
    path('set-cookie/', set_cookie_view, name='set_cookie'),
]

