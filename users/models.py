from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.measure import D
from django.db.models.signals import post_save
from django.dispatch import receiver
import hashlib


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(
        max_length=30, blank=True, null=True, default=None)

    def get_total_miles(self):
        miles = self.user.run_set.filter(units='mi').aggregate(
            miles=models.Sum('distance'))['miles'] or 0
        kms = self.user.run_set.filter(units='km').aggregate(
            kms=models.Sum('distance'))['kms'] or 0
        km_mi = D(km=kms).mi
        return round(float(miles) + float(km_mi), 2)

    def gravatar_url(self):
        md5 = hashlib.md5(self.user.email.encode())
        digest = md5.hexdigest()

        return f'http://www.gravatar.com/avatar/{digest}'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
