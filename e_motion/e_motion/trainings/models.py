from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()


class Training(models.Model):

    title = models.CharField(
        unique=True,
        max_length=100
    )

    description = models.TextField()

    picture = models.URLField()

    instructor = models.ForeignKey(
        to=UserModel,
        on_delete=models.SET_NULL,
        null=True,
        related_name='instructor',
    )

    def __str__(self):
        return f"{self.title}"
