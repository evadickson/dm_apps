# Generated by Django 2.1.4 on 2019-04-23 18:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('herring', '0002_auto_20190423_1349'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='district',
            name='alias_port_name',
        ),
        migrations.RemoveField(
            model_name='district',
            name='alias_wharf_id',
        ),
    ]