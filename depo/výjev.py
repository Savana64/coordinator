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
            print(form.errors)  # Debugging chyb ve formuláři
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