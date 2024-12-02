# Generated by Django 5.1.3 on 2024-12-02 16:19

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trainings', '0003_alter_training_instructor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='training',
            name='picture',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='image'),
        ),
    ]
