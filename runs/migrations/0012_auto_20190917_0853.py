# Generated by Django 2.2.4 on 2019-09-17 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('runs', '0011_auto_20190826_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='run',
            name='run_type',
            field=models.CharField(blank=True, choices=[('Canicross', 'Canicross'), ('Road run', 'Road run'), ('Long run', 'Long run'), ('Trail run', 'Trail run'), ('Race', 'Race'), ('Treadmill', 'Treadmill')], default=None, max_length=10, null=True),
        ),
    ]
