# Generated by Django 2.0.4 on 2018-11-09 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('camp', '0009_auto_20181109_1112'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='speciesobservations',
            name='count_adults',
        ),
        migrations.RemoveField(
            model_name='speciesobservations',
            name='count_total',
        ),
        migrations.RemoveField(
            model_name='speciesobservations',
            name='count_unknown',
        ),
        migrations.RemoveField(
            model_name='speciesobservations',
            name='count_yoy',
        ),
        migrations.AddField(
            model_name='speciesobservations',
            name='adults',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='speciesobservations',
            name='total',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='speciesobservations',
            name='unknown',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='speciesobservations',
            name='yoy',
            field=models.FloatField(default=0),
        ),
    ]
