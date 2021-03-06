from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.measure import D
from django.core.validators import MinValueValidator
from django.shortcuts import reverse
from django.utils import timezone
from datetime import timedelta


class Gear(models.Model):
    '''
    For now, this will be used for running shoes.
    I may expand to include other types of gear in
    the future.
    '''
    _unit_choices = (('mi', 'mi'), ('km', 'km'))

    name = models.TextField(max_length=30)
    start_distance = models.DecimalField(
        max_digits=5, decimal_places=2,
        default=0.0, blank=True, null=True,
        validators=[MinValueValidator(0.0)])
    start_units = models.CharField(
        max_length=2, choices=_unit_choices, default='mi')
    date_added = models.DateTimeField(default=timezone.now)
    date_retired = models.DateTimeField(null=True, blank=True, default=None)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date_added']

    def get_starting_miles(self):
        if self.start_units == 'km':
            return round(float(D(km=self.start_distance).mi), 2)
        return round(float(self.start_distance), 2)

    def get_total_miles(self):
        miles = self.run_set.filter(units='mi').aggregate(
            miles=models.Sum('distance'))['miles'] or 0
        kms = self.run_set.filter(units='km').aggregate(
            kms=models.Sum('distance'))['kms'] or 0
        km_mi = D(km=kms).mi
        return round(
            float(miles) + float(km_mi) + self.get_starting_miles(), 2)

    def get_absolute_url(self):
        return reverse('runs:gear-detail', kwargs={'pk': self.id})

    def __str__(self):
        return self.name


class Run(models.Model):
    _unit_choices = (('mi', 'mi'), ('km', 'km'))
    _run_choices = (
        ('Canicross', 'Canicross'),
        ('Road run', 'Road run'),
        ('Long run', 'Long run'),
        ('Trail run', 'Trail run'),
        ('Race', 'Race'),
        ('Treadmill', 'Treadmill'))

    run_date = models.DateTimeField(default=timezone.now)
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
        ordering = ['-run_date']

    def get_duration(self):
        if self.duration is not None and self.duration.seconds // 3600 == 0:
            minutes = self.duration.seconds // 60
            seconds = self.duration.seconds - (minutes * 60)
            return f'{minutes}:{seconds:02}'
        return self.duration

    def get_pace(self):
        if self.duration is None:
            return None
        pace = self.duration / float(self.distance)
        pace = pace - timedelta(microseconds=pace.microseconds)
        if pace.seconds // 3600 == 0:
            minutes = pace.seconds // 60
            seconds = pace.seconds - (minutes * 60)
            return f'{minutes}:{seconds:02}'
        return pace

    def __str__(self):
        return f'{self.run_date}, {self.distance}{self.units}'
