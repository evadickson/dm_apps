# Generated by Django 3.2.5 on 2021-11-05 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scuba', '0009_auto_20211105_1025'),
    ]

    operations = [
        migrations.AddField(
            model_name='dive',
            name='is_upm',
            field=models.BooleanField(default=False, verbose_name='was this a UPM dive?'),
        ),
        migrations.AlterUniqueTogether(
            name='diver',
            unique_together={('first_name', 'last_name')},
        ),
        migrations.RemoveField(
            model_name='diver',
            name='is_upm',
        ),
    ]