from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.measure import D
from django.core.validators import MinValueValidator
from django.shortcuts import reverse
from django.utils import timezone


class Gear(models.Model):
    '''
    For now, this will be used for running shoes.
    I may expand to include other types of gear in
    the future.
    '''
    name = models.TextField(max_length=30)
    date_added = models.DateField(default=timezone.now)
    date_retired = models.DateField(null=True, blank=True, default=None)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date_added']

    def get_total_miles(self):
        miles = self.run_set.filter(units='mi').aggregate(
            miles=models.Sum('distance'))['miles'] or 0
        kms = self.run_set.filter(units='km').aggregate(
            kms=models.Sum('distance'))['kms'] or 0
        km_mi = D(km=kms).mi
        return round(float(miles) + float(km_mi), 2)

    def get_absolute_url(self):
        return reverse('runs:gear-detail', kwargs={'pk': self.id})

    def __str__(self):
        return self.name


class Run(models.Model):
    _unit_choices = (('mi', 'mi'), ('km', 'km'))
    _run_choices = (
        ('Road run', 'Road run'),
        ('Trail run', 'Trail run'),
        ('Race', 'Race'),
        ('Treadmill', 'Treadmill'))

    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)  # for better sotring
    distance = models.DecimalField(
        max_digits=5, decimal_places=2,
        validators=[MinValueValidator(0.0)])
    units = models.CharField(max_length=2, choices=_unit_choices)
    duration = models.DurationField(
        default=None, blank=True, null=True)
    description = models.CharField(
        max_length=240, default=None, blank=True, null=True)
    run_type = models.CharField(
        max_length=10, default=None, blank=True, null=True,
        choices=_run_choices)

    gear = models.ForeignKey(
        Gear, on_delete=models.SET_NULL,
        null=True, blank=True, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date', '-time']

    def __str__(self):
        return f'{self.date}, {self.distance}{self.units}'
