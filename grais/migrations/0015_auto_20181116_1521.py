# Generated by Django 2.0.4 on 2018-11-16 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grais', '0014_auto_20181116_1427'),
    ]

    operations = [
        migrations.AlterField(
            model_name='surface',
            name='label',
            field=models.CharField(max_length=255),
        ),
    ]