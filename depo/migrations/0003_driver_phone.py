# Generated by Django 5.1.3 on 2024-11-21 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('depo', '0002_driver_is_on_rest'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='phone',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
