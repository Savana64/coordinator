from django.db import models
from django.utils import timezone
from datetime import timedelta

# Model pro autobus
class Bus(models.Model):
    name = models.CharField(max_length=100)
    seats = models.CharField(max_length=10)  # např. "45+1"
    is_ready = models.BooleanField(default=True)  # indikace dostupnosti autobusu

    def __str__(self):
        return self.name

# Model pro řidiče
class Driver(models.Model):
    name = models.CharField(max_length=100)
    last_rest_day = models.DateField(default=timezone.now)  # poslední den volna

    def days_since_last_rest(self):
        # Spočítá, kolik dní uplynulo od posledního volna
        return (timezone.now().date() - self.last_rest_day).days

    def needs_rest(self):
        # Kontrola, zda má mít den volna po 6 dnech
        days_worked = (timezone.now().date() - self.last_rest_day).days
        return days_worked >= 6

    def needs_daily_rest(self, last_drive_end):
        # Kontrola, zda má denní odpočinek minimálně 11 hodin (9 hodin dvakrát týdně)
        rest_period = timedelta(hours=11)  # defaultní odpočinek 11 hodin
        daily_drives = self.reservation_set.filter(
            end_time__gte=last_drive_end - rest_period
        )
        return daily_drives.count() <= 2  # Pokud je 9 hodin odpočinku povoleno dvakrát týdně

    def __str__(self):
        return self.name

# Model pro rezervaci
class Reservation(models.Model):
    name = models.CharField(max_length=100)  # pro koho se jede
    start_time = models.DateTimeField()  # kdy se začíná
    end_time = models.DateTimeField()    # kdy končí
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.bus.name} - {self.driver.name}"

