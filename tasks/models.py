from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    INTERVAL_CHOICES = [
        ('hour', 'Hourly'),
        ('day', 'Daily'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)
    task = models.TextField(max_length=600, blank=True)
    deadline = models.DateTimeField()
    email = models.CharField(max_length=255, blank=True, null=True)
    notification_interval = models.CharField(max_length=50, blank=True, choices=INTERVAL_CHOICES, null=True)
    notification_time = models.TimeField(blank=True, null=True)

    def __str__(self):
        return self.name


