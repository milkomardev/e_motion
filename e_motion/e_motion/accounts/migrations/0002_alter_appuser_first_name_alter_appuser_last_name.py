# Generated by Django 5.1.3 on 2024-11-16 15:50

import e_motion.accounts.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appuser',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, validators=[e_motion.accounts.validators.CapitalizedValidator()]),
        ),
        migrations.AlterField(
            model_name='appuser',
            name='last_name',
            field=models.CharField(blank=True, max_length=150, validators=[e_motion.accounts.validators.CapitalizedValidator()]),
        ),
    ]