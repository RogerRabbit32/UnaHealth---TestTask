from django.db import models
from django.contrib.auth.models import User


class GlucoseLevel(models.Model):
    TEST_TYPE_CHOICES = [
        (0, 'Automatic transmission'),
        (1, 'Sensor scan'),
        (6, 'No glucose level data'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='glucose_levels',
    )

    device_name = models.CharField(
        max_length=100,
    )

    device_serial_number = models.CharField(
        max_length=36,
    )

    timestamp = models.DateTimeField()

    recording_type = models.IntegerField(
        choices=TEST_TYPE_CHOICES,
    )

    glucose_value = models.PositiveIntegerField(
        null=True,
    )

    def __str__(self):
        return f"Glucose Level {self.id} for User {self.user.username}"
