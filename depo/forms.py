from django import forms
from .models import Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['name', 'start_time', 'end_time', 'bus', 'driver']
