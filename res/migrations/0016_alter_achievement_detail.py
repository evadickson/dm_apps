# Generated by Django 3.2.4 on 2021-10-18 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('res', '0015_auto_20211015_1540'),
    ]

    operations = [
        migrations.AlterField(
            model_name='achievement',
            name='detail',
            field=models.CharField(blank=True, max_length=2000, null=True, verbose_name='detail'),
        ),
    ]