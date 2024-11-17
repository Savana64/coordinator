from django import forms
from django.utils import timezone
from datetime import timedelta
from .models import Bus, Driver, Reservation


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['name', 'bus','start_time', 'end_time',  'driver' ]
        labels = {
            'name': 'Název rezervace',
            'bus': 'Autobus',
            'start_time': 'Čas začátku',
            'end_time': 'Čas konce',
            'driver': 'Řidič',
        }
        widgets = {
            'start_time': forms.DateTimeInput(
                attrs={'placeholder': 'dd.mm.rrrr hh:mm', 'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
            'end_time': forms.DateTimeInput(
                attrs={'placeholder': 'dd.mm.rrrr hh:mm', 'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
        }
    # Definice dynamicky filtrovaných polí
    bus = forms.ModelChoiceField(queryset=Bus.objects.none(), label="Autobus")
    driver = forms.ModelChoiceField(queryset=Driver.objects.none(), label="Řidič")
    # Definujeme formáty pro start_time a end_time
    input_formats = {
        'start_time': ['%Y-%m-%dT%H:%M', '%d.%m.%Y %H:%M'],
        'end_time': ['%Y-%m-%dT%H:%M', '%d.%m.%Y %H:%M'],
    }

    def __init__(self, *args, **kwargs):
        available_buses = kwargs.pop('available_buses', Bus.objects.filter(is_ready=True))
        available_drivers = kwargs.pop(
            'available_drivers',
            Driver.objects.filter(
                is_on_rest=False,
                last_rest_day__gte=timezone.now().date() - timedelta(days=6)
            )
        )
        super().__init__(*args, **kwargs)
        self.fields['bus'].queryset = available_buses
        self.fields['driver'].queryset = available_drivers


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
