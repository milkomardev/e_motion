from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import DateTimeField
from django.utils.timezone import now
from django.db.models import F, ExpressionWrapper

UserModel = get_user_model()


class ScheduleQuerySet(models.QuerySet):
    def annotate_with_end_time(self):
        return self.annotate(
            date__add_duration=ExpressionWrapper(
                F('date') + F('duration'),
                output_field=DateTimeField()
            )
        )


class Schedule(models.Model):
    training = models.ForeignKey(
        'trainings.Training',
        on_delete=models.SET_NULL,
        related_name='scheduled_instances',
        null=True,
    )

    training_title = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    instructor_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    date = models.DateTimeField()

    duration = models.DurationField(
        default=timedelta(hours=1)
    )

    students = models.ManyToManyField(
        to=UserModel,
        related_name='scheduled_trainings',
        blank=True,
    )

    max_attendees = models.PositiveIntegerField(default=20)

    waiting_list = models.ManyToManyField(
        to=UserModel,
        related_name='waiting_list_trainings',
        blank=True,
    )

    objects = ScheduleQuerySet.as_manager()

    def clean(self):
        end_time = self.end_time()
        overlapping_schedules = Schedule.objects.annotate_with_end_time().filter(
            date__lt=end_time,
            date__add_duration__gt=self.date
        ).exclude(pk=self.pk)

        if overlapping_schedules.exists():
            raise ValidationError('This training overlaps with another training in the schedule.')

    def save(self, *args, **kwargs):
        self.clean()

        if self.training:
            self.training_title = self.training.title
            self.instructor_name = self.training.instructor.user.get_full_name()
            self.end_time = self.date + self.duration

        super(Schedule, self).save(*args, **kwargs)

    def end_time(self):
        return self.date + self.duration

    def can_cancel(self):
        return self.date - timedelta(hours=3) > now()

    def is_full(self):
        return self.students.count() >= self.max_attendees

    def has_passed(self):
        return now() > self.end_time()

    def user_waiting_list_position(self, user):
        if user in self.waiting_list.all():
            return list(self.waiting_list.all()).index(user) + 1
        return None

    def __str__(self):
        return f"{self.training.title} on {self.date.strftime('%Y-%m-%d %H:%M')}"
