# Generated by Django 2.1.4 on 2019-03-27 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grais', '0011_auto_20190327_1548'),
    ]

    operations = [
        migrations.AddField(
            model_name='crab',
            name='sex',
            field=models.IntegerField(blank=True, choices=[(1, 'Male'), (2, 'Female')], null=True),
        ),
    ]
