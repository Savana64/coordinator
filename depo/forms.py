from django import forms
from .models import Bus, Driver, Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['name', 'start_time', 'end_time', 'bus', 'driver' ]
        labels = {
            'name': 'Název rezervace',
            'bus': 'Autobus',
            'start_time': 'Čas začátku',
            'end_time': 'Čas konce',
            'driver': 'Řidič',
        }

    # Definice dynamicky filtrovaných polí
    bus = forms.ModelChoiceField(queryset=Bus.objects.none(), label="Autobus")
    driver = forms.ModelChoiceField(queryset=Driver.objects.none(), label="Řidič")


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
