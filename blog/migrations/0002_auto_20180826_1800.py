# Generated by Django 2.0.7 on 2018-08-26 13:30

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 8, 26, 13, 30, 22, 706625, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2018, 8, 26, 13, 30, 22, 705625, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='expiration_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 8, 27, 13, 30, 22, 705625, tzinfo=utc)),
        ),
    ]
