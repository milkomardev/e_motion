# Generated by Django 5.1.3 on 2024-11-26 16:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='duration',
            field=models.DurationField(default=datetime.timedelta(seconds=3600)),
        ),
    ]
