from datetime import timezone

from django.contrib.auth import get_user_model
from django.db import models

from e_motion.accounts.choices import SubscriptionChoices, AttendanceLimitChoices
from e_motion.accounts.validators import PhoneNumberValidator

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

    profile_picture = models.URLField(
        blank=True,
        null=True,
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

    # This field is used to keep track of the number of times a user has not attended a class for which he booked a slot
    non_attendance_count = models.PositiveIntegerField(default=0)

    # enrolled_trainings = models.ManyToManyField(
    #     to='trainings.TrainingSession',
    #     related_name='enrolled_trainings',
    #     blank=True,
    # )
    #
    # attended_trainings = models.ManyToManyField(
    #     to='trainings.TrainingSession',
    #     related_name='attended_trainings',
    #     blank=True,
    # )
    #
    # def next_class(self):
    #     """Returns the next class the student is enrolled in."""
    #     return self.enrolled_trainings.filter(date__gte=timezone.now()).order_by('date').first()

    def __str__(self):
        return f"{self.user.username}'s Profile"


