from django.urls import path
from . import views

app_name = 'depo'

urlpatterns = [
    path('', views.home, name='home'),
    path('buses/', views.bus_list, name='bus_list'),
    path('drivers/', views.driver_list, name='driver_list'),
    path('reservations/', views.reservation_list, name='reservation_list'),
    path('add_reservation/', views.add_reservation, name='add_reservation'),
]

