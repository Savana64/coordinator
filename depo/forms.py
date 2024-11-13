from django import forms
from .models import Bus, Driver, Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['name', 'bus', 'start_time', 'end_time', 'driver']

    # Definice dynamicky filtrovaných polí
    bus = forms.ModelChoiceField(queryset=Bus.objects.none())
    driver = forms.ModelChoiceField(queryset=Driver.objects.none())


class RestStatusForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['is_on_rest']
        widgets = {
            'is_on_rest': forms.CheckboxInput(),
        }

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
