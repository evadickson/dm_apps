# Generated by Django 3.1.2 on 2020-11-03 15:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whalebrary', '0018_auto_20201030_1222'),
    ]

    operations = [
        migrations.AddField(
            model_name='incident',
            name='date_email_sent',
            field=models.DateTimeField(blank=True, null=True, verbose_name='date incident emailed'),
        ),
        migrations.AlterField(
            model_name='order',
            name='date_ordered',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 3, 11, 57, 59, 322071), verbose_name='order date'),
        ),
    ]
