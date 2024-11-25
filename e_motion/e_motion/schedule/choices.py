from django.db import models
from datetime import timedelta


class DurationChoices(models.TextChoices):
    HALF_HOUR = str(timedelta(hours=0, minutes=30)), "30 minutes"
    ONE_HOUR = str(timedelta(hours=1)), "1 hour"
    ONE_HALF_HOUR = str(timedelta(hours=1, minutes=30)), "1 hour 30 minutes"
    TWO_HOURS = str(timedelta(hours=2)), "2 hours"