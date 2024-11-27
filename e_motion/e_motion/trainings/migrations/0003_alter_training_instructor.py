# Generated by Django 5.1.3 on 2024-11-27 19:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instructors', '0001_initial'),
        ('trainings', '0002_alter_training_instructor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='training',
            name='instructor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='trainings', to='instructors.instructor'),
        ),
    ]