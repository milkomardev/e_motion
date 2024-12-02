from django.utils.timezone import now

from django.contrib.auth import get_user_model
from django.db import models

from e_motion.accounts.choices import SubscriptionChoices, AttendanceLimitChoices
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

    subscription_active = models.BooleanField(
        default=False,
    )

    subscription_plan = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        choices=SubscriptionChoices.choices,
    )

    attendance_limit = models.PositiveIntegerField(default=0, choices=AttendanceLimitChoices.choices)
    attendance_count = models.PositiveIntegerField(default=0)

    attended_trainings = models.ManyToManyField(
        to='schedule.Schedule',
        related_name='attended_trainings',
        blank=True,
    )

    def next_training(self):
        return self.user.scheduled_trainings.filter(date__gte=now()).order_by('date').first()

    def __str__(self):
        return f"{self.user.get_full_name()}'s Profile"


