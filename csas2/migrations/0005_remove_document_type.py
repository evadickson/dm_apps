# Generated by Django 3.2 on 2021-04-30 17:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('csas2', '0004_auto_20210430_1417'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='type',
        ),
    ]