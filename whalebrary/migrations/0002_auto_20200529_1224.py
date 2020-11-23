# Generated by Django 2.2.2 on 2020-05-29 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whalebrary', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='incident',
        ),
        migrations.AddField(
            model_name='transaction',
            name='incident',
            field=models.ManyToManyField(blank=True, to='whalebrary.Incident', verbose_name='incident'),
        ),
    ]
