# Generated by Django 2.2.2 on 2019-06-17 17:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spot', '0049_activity_program'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='priority_area_or_threat',
        ),
    ]