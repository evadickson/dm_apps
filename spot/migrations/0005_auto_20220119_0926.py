# Generated by Django 3.1.2 on 2022-01-19 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spot', '0004_auto_20220119_0909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='agreement_history',
            field=models.ManyToManyField(blank=True, to='spot.Project', verbose_name='Agreement History'),
        ),
    ]
