# Generated by Django 2.1.4 on 2019-01-14 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='fiscal_year',
            field=models.CharField(default='2019-2020', max_length=50),
        ),
    ]