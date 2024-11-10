from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Bus, Driver, Reservation
from .forms import ReservationForm

# Hlavní stránka s odkazem na přihlášení a zobrazení rezervací
def home(request):
    return render(request, 'depo/home.html')

# Zobrazení seznamu autobusů
def bus_list(request):
    buses = Bus.objects.all()
    return render(request, 'depo/bus_list.html', {'buses': buses})

# Zobrazení seznamu řidičů
def driver_list(request):
    drivers = Driver.objects.all()
    return render(request, 'depo/driver_list.html', {'drivers': drivers})

# Zobrazení seznamu rezervací
def reservation_list(request):
    reservations = Reservation.objects.all()
    return render(request, 'depo/reservation_list.html', {'reservations': reservations})

# Přidání nové rezervace
# views.py
def add_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            # Nastaví nové volno řidiče po ukončení pracovního týdne
            if reservation.driver.days_since_last_rest() >= 6:
                reservation.driver.last_rest_day = timezone.now()
            reservation.save()
            return redirect('depo/reservation_list')
    else:
        form = ReservationForm()
    return render(request, 'depo/reservation_form.html', {'form': form})



# Create your views here.
