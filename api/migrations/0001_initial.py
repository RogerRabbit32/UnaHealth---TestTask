# Generated by Django 4.2.13 on 2024-06-26 17:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GlucoseLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_name', models.CharField(max_length=100)),
                ('device_serial_number', models.CharField(max_length=36)),
                ('timestamp', models.DateTimeField()),
                ('recording_type', models.IntegerField(choices=[(0, 'Automatic transmission'), (1, 'Sensor scan'), (6, 'No glucose level data')])),
                ('glucose_value', models.PositiveIntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='glucose_levels', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]