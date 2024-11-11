from django import forms
from .models import Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['name', 'start_time', 'end_time', 'bus', 'driver']

 # Přidáme widgety s placeholdery
        #widgets = {
            #'start_time': forms.TimeInput(attrs={'placeholder': 'hh:mm', 'type': 'time'}),
            #'end_time': forms.TimeInput(attrs={'placeholder': 'hh:mm', 'type': 'time'}),
        #}

      # Přidáme widgety s placeholdery pro datum i čas
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'placeholder': 'dd.mm.rrrr hh:mm', 'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'placeholder': 'dd.mm.rrrr hh:mm', 'type': 'datetime-local'}),
        }
