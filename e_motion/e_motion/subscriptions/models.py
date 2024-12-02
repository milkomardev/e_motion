from django.db import models


class SubscriptionPlan(models.Model):
    name = models.CharField(
        max_length=100
    )

    duration_months = models.PositiveIntegerField(
        default=1
    )

    attendance_limit = models.PositiveIntegerField()

    price_per_training = models.DecimalField(
        default=0,
        max_digits=5,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.duration_months} months - {self.attendance_limit} attendances"

