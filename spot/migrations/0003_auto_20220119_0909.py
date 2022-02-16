# Generated by Django 3.1.2 on 2022-01-19 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spot', '0002_auto_20220111_0923'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='cu_index',
        ),
        migrations.AddField(
            model_name='project',
            name='cu_index',
            field=models.ManyToManyField(blank=True, null=True, to='spot.CUIndex', verbose_name='CU Index'),
        ),
    ]