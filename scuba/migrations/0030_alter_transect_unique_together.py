# Generated by Django 3.2.5 on 2021-12-06 17:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scuba', '0029_transect_new_name'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='transect',
            unique_together=set(),
        ),
    ]