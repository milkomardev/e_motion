from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()


class Training(models.Model):

    title = models.CharField(
        unique=True,
        max_length=100
    )

    description = models.TextField()

    picture = CloudinaryField("image")

    instructor = models.ForeignKey(
        to='instructors.Instructor',
        on_delete=models.CASCADE,
        null=True,
        related_name='trainings',
    )

    def __str__(self):
        return f"{self.title}"
