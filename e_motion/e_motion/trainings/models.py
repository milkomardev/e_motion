from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify

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

    slug = models.SlugField(
        null=True,
        blank=True,
        unique=True,
        editable=False,
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}"
