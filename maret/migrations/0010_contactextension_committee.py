# Generated by Django 3.2.5 on 2021-12-16 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maret', '0009_auto_20211208_1326'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactextension',
            name='committee',
            field=models.ManyToManyField(blank=True, related_name='contact_committees', to='maret.Committee', verbose_name='Committee / Working Group Membership'),
        ),
    ]
