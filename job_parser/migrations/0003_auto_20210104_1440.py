# Generated by Django 3.1.4 on 2021-01-04 11:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_parser', '0002_auto_20210104_1439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 1, 4, 14, 40, 54, 144425)),
        ),
    ]