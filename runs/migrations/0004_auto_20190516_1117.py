# Generated by Django 2.2 on 2019-05-16 17:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('runs', '0003_auto_20190514_1022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='run',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]