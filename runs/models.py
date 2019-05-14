from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
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

    def __str__(self):
        return f'{self.name} owned by {self.owner.username}'


class Run(models.Model):
    _unit_choices = (('mi', 'mi'), ('km', 'km'))

    date = models.DateTimeField(default=timezone.now)
    distance = models.DecimalField(
        max_digits=5, decimal_places=2,
        validators=[MinValueValidator(0.0)])
    units = models.CharField(max_length=2, choices=_unit_choices)
    duration = models.DurationField(
        default=None, blank=True, null=True)
    gear = models.ForeignKey(
        Gear, on_delete=models.SET_NULL,
        null=True, blank=True, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.date}, {self.distance}{self.units}'

    def get_duration_seconds(self):
        """
        Returns the total duration in seconds.
        """
        return self.duration.seconds \
            + self.duration.minutes*60 \
            + self.duration.hours*3600
