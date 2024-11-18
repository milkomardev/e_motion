from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()


class TrainingSchedule(models.Model):
    title = models.CharField(
        max_length=100
    )

    description = models.TextField()
    date = models.DateTimeField()

    picture = models.URLField()

    instructor = models.ForeignKey(
        to=UserModel,
        on_delete=models.SET_NULL,
        null=True,
        related_name='instructor',
    )

    students = models.ManyToManyField(
        to=UserModel,
        related_name='enrolled_trainings',
        blank=True,
    )

    def __str__(self):
        return f"{self.title} on {self.date}"
