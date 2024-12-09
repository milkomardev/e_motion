from django.utils.timezone import now

from django.contrib.auth import get_user_model
from django.db import models
from datetime import timedelta

from e_motion.accounts.validators import PhoneNumberValidator

from cloudinary.models import CloudinaryField

UserModel = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(
        to=UserModel,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    phone_number = models.CharField(
        max_length=15,
        validators=[PhoneNumberValidator(),],
        blank=True,
        null=True,
    )

    date_of_birth = models.DateField(
        blank=True,
        null=True,
    )

    profile_picture = CloudinaryField(
        "image",
        blank=True,
        null=True
    )

    subscription_start_date = models.DateField(
        blank=True,
        null=True,
    )

    subscription_end_date = models.DateField(
        blank=True,
        null=True,
    )

    subscription_plan = models.ForeignKey(
        to="subscriptions.SubscriptionPlan",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    attendance_count = models.PositiveIntegerField(default=0)

    attended_trainings = models.ManyToManyField(
        to='schedule.Schedule',
        related_name='attended_trainings',
        blank=True,
    )

    def next_training(self):
        return self.user.scheduled_trainings.filter(date__gte=now()).order_by('date').first()

    def save(self, *args, **kwargs):
        if self.subscription_plan and self.subscription_start_date:
            duration = timedelta(days=30 * self.subscription_plan.duration_months)
            self.subscription_end_date = self.subscription_start_date + duration
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.get_full_name()}'s Profile"


