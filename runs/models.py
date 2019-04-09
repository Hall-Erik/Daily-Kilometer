from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone


class Run(models.Model):
    _unit_choices = (('mi', 'mi'), ('km', 'km'))

    date = models.DateTimeField(default=timezone.now)
    distance = models.DecimalField(
        max_digits=5, decimal_places=2,
        validators=[MinValueValidator(0.0)])
    units = models.CharField(max_length=2, choices=_unit_choices)
    hours = models.IntegerField(
        default=None, blank=True, null=True,
        validators=[MinValueValidator(0)])
    minutes = models.IntegerField(
        default=None, blank=True, null=True,
        validators=[MinValueValidator(0), MaxValueValidator(59)])
    seconds = models.IntegerField(
        default=None, blank=True, null=True,
        validators=[MinValueValidator(0), MaxValueValidator(59)])
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'<Run {self.date}, {self.distance}{self.units}>'

    def get_duration_seconds(self):
        """
        Returns the total duration in seconds.
        """
        return self.seconds + self.minutes*60 + self.hours*3600

# class Shoe(models.Model):
#     name = models.TextField('Gear', max_length=20)