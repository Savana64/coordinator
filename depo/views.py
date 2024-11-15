from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from datetime import timedelta
from .models import Bus, Driver, Reservation
from .forms import ReservationForm, RestStatusForm
from django.contrib.auth.forms import UserCreationForm


# Hlavní stránka s odkazem na přihlášení a zobrazení rezervací
def home(request):
    return render(request, 'depo/home.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('depo/login')
    else:
        form = UserCreationForm()
    return render(request, 'depo/register.html', {'form': form})

# Zobrazení seznamu autobusů

def bus_list(request):
    buses = Bus.objects.all()
     # Ošetření změny stavu dostupnosti autobusu
    if request.method == 'POST':
        bus_id = request.POST.get('bus_id')
        bus = Bus.objects.get(id=bus_id)
        bus.toggle_is_ready()  # Přepne stav dostupnosti autobusu
        return redirect('depo:bus_list')  # Přesměrování zpět na seznam autobusů
    return render(request, 'depo/bus_list.html', {'buses': buses})

# Zobrazení seznamu řidičů
@login_required
def driver_list(request):
    drivers = Driver.objects.all()
    
    # Nastavení volna řidiče přes formulář
    if request.method == 'POST':
        driver_id = request.POST.get('driver_id')
        driver = get_object_or_404(Driver, id=driver_id)
        #form = RestStatusForm(request.POST, instance=driver)
        # Přepnutí stavu volna
        driver.is_on_rest = not driver.is_on_rest
        if driver.is_on_rest:
            driver.last_rest_day = timezone.now().date()  # Nastavení dne volna, pokud řidič jde na volno
        driver.save()
        #if form.is_valid():
            #form.save()
        return redirect('depo:driver_list')  # Přesměrování zpět na seznam řidičů
    
    return render(request, 'depo/driver_list.html', {'drivers': drivers})

# Zobrazení seznamu rezervací
@login_required
def reservation_list(request):
    reservations = Reservation.objects.all()
    return render(request, 'depo/reservation_list.html', {'reservations': reservations})

# Přidání nové rezervace
# views.py

@login_required
def add_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            if reservation.driver.days_since_last_rest() >= 6:
                reservation.driver.last_rest_day = timezone.now()
                reservation.driver.is_on_rest = True
                reservation.driver.save()
            reservation.save()
            return redirect('depo:reservation_list')
    else:
        # Filtrování dostupných autobusů a řidičů
        available_buses = Bus.objects.filter(is_ready=True)
        # Filtrování řidičů, kteří jsou "v práci" (1 až 6 dní od posledního volna)
        available_drivers = Driver.objects.filter(
            is_on_rest=False,
            last_rest_day__gte=timezone.now().date() - timedelta(days=6)
        )

        form = ReservationForm()
        form.fields['bus'].queryset = available_buses
        form.fields['driver'].queryset = available_drivers

    return render(request, 'depo/reservation_form.html', {'form': form})



def delete_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    reservation.delete()
    return redirect('depo:reservation_list')


# Create your views here.
