# Generated by Django 3.2.5 on 2021-11-12 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scuba', '0012_species'),
    ]

    operations = [
        migrations.AlterField(
            model_name='species',
            name='code',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]