# Generated by Django 2.0.2 on 2018-10-10 15:27

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0002_auto_20181010_1523'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='date_of_exp',
            field=models.DateField(default=datetime.datetime(2018, 10, 10, 15, 27, 26, 508543, tzinfo=utc)),
        ),
    ]
