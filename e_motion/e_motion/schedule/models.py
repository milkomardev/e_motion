from django.contrib.auth import get_user_model
from django.db import models
from django.utils.timezone import now

UserModel = get_user_model()


class Schedule(models.Model):
    training = models.ForeignKey(
        'trainings.Training',
        on_delete=models.CASCADE,
        related_name='scheduled_instances',
    )

    date = models.DateTimeField()

    duration = models.DurationField()

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

    def end_time(self):
        return self.date + self.duration

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
