# Generated by Django 2.0.4 on 2018-12-05 17:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oceanography', '0014_auto_20181205_1346'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bottle',
            old_name='sal',
            new_name='salinity',
        ),
    ]
