# Generated by Django 2.0.4 on 2018-11-09 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('camp', '0008_auto_20181109_1049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sample',
            name='mean_sediment_grain_size',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
