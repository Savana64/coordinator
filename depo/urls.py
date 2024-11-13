from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
app_name = 'depo'

urlpatterns = [
    path('', views.home, name='home'),
    path('buses/', views.bus_list, name='bus_list'),
    path('drivers/', views.driver_list, name='driver_list'),
    path('reservations/', views.reservation_list, name='reservation_list'),
    path('reservations/delete/<int:reservation_id>/', views.delete_reservation, name='delete_reservation'),
    path('add_reservation/', views.add_reservation, name='add_reservation'),
    path('login/', auth_views.LoginView.as_view(template_name='depo/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view( template_name='depo/logout.html'), name='logout'),
    path('register/', views.register, name='register')
]

