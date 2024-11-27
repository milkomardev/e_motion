from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()


class Instructor(models.Model):
    user = models.OneToOneField(
        to=UserModel,
        on_delete=models.CASCADE,
        related_name='instructor_profile'
    )

    bio = models.TextField()

    def __str__(self):
        return self.user.get_full_name()