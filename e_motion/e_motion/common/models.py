from cloudinary.models import CloudinaryField
from django.db import models


class ContactInfo(models.Model):
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()

    def __str__(self):
        return "Contact Information"


class GalleryImage(models.Model):
    image = CloudinaryField('image')

    title = models.CharField(
        max_length=100,
    )

    description = models.TextField(
        blank=True,
        null=True,
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.description or "Image"
