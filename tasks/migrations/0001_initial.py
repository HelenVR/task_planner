# Generated by Django 5.0.7 on 2024-07-14 14:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Task",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255, unique=True)),
                ("task", models.JSONField()),
                ("deadline", models.DateTimeField()),
                (
                    "telegram_nick",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "notification_interval",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                ("notification_time", models.TimeField(blank=True, null=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
