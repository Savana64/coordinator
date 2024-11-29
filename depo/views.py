from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from datetime import timedelta
from .models import Bus, Driver, Reservation
from .forms import ReservationForm
from django.contrib.auth.forms import UserCreationForm


# Hlavní stránka s odkazem na přihlášení a zobrazení rezervací
def home(request):
    return render(request, 'depo/home.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        next_url = request.POST.get("next", "/depo/home/")  # Výchozí stránka (např. domovská stránka)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(next_url)  # Přesměruje na stránku z `next`, nebo na výchozí
        else:
            return render(request, "depo/login.html", {
                "error": "Špatné uživatelské jméno nebo heslo",
                "next": next_url,  # Vrátí zpět `next` pro opětovné zobrazení ve formuláři
            })
    
    return render(request, "depo/login.html", {
        "next": request.GET.get("next", "/depo/home/"),  # Výchozí stránka při načtení formuláře
    })

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request, user)
            next_url = request.GET.get('next', 'depo:home') # Získej původní URL nebo přesměruj na domovskou stránku
            return redirect(next_url)
    else:
        form = UserCreationForm()
    return render(request, 'depo/register.html', {'form': form})

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        next_url = request.POST.get("next", "/depo/home/")  # Výchozí stránka

        if password1 == password2:
            user = User.objects.create_user(username=username, password=password1)
            login(request, user)  # Automatické přihlášení po registraci
            return HttpResponseRedirect(next_url)
        else:
            return render(request, "depo/register.html", {
                "error": "Hesla se neshodují",
                "next": next_url,  # Vrátí zpět `next` pro opětovné zobrazení ve formuláři
            })
    
    return render(request, "depo/register.html", {
        "next": request.GET.get("next", "/depo/home/"),  # Výchozí stránka při načtení formuláře
    })

def set_cookie_view(request):
    response = HttpResponse("Cookies byly nastaveny.")
    response.set_cookie('moje_cookie', 'hodnota_cookie', max_age=3600)  # Platnost 1 hodina
    return response

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
    reservations = Reservation.objects.all().order_by('-start_time')
    return render(request, 'depo/reservation_list.html', {'reservations': reservations})

# Přidání nové rezervace
# views.py

@login_required
def add_reservation(request):
    # Filtr dostupných autobusů a řidičů
    available_buses = Bus.objects.filter(is_ready=True)
    available_drivers = Driver.objects.filter(
        is_on_rest=False,
        last_rest_day__gte=timezone.now().date() - timedelta(days=6)
    )

    if request.method == 'POST':
        form = ReservationForm(request.POST, available_buses=available_buses, available_drivers=available_drivers)
        if form.is_valid():
            reservation = form.save(commit=False)
            # Aktualizace stavu řidiče
            if reservation.driver.days_since_last_rest() >= 6:
                reservation.driver.last_rest_day = timezone.now()
                reservation.driver.is_on_rest = True
                reservation.driver.save()
            reservation.save()
            return redirect('depo:reservation_list')
    else:
        form = ReservationForm(available_buses=available_buses, available_drivers=available_drivers)

    return render(request, 'depo/reservation_form.html', {'form': form})




def delete_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    reservation.delete()
    return redirect('depo:reservation_list')

@login_required
def update_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            return redirect('depo:reservation_list')
    else:
        form = ReservationForm(instance=reservation)

    return render(request, 'depo/reservation_form.html', {'form': form})


def about(request):
    return render(request, 'depo/about.html')
# Create your views here.
