# Generated by Django 2.1.4 on 2019-02-18 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0032_remove_gccost_funding_source'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='lead',
            field=models.BooleanField(default=1, verbose_name='project lead'),
            preserve_default=False,
        ),
    ]