# Generated by Django 2.1.4 on 2019-02-13 18:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ihub', '0016_auto_20190213_1315'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entry',
            name='leads',
        ),
    ]
