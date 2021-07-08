# Generated by Django 3.2 on 2021-05-21 10:41

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('csas2', '0027_process_editors'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='time_description_en',
            field=models.CharField(blank=True, default='9am to 4pm (Atlantic)', help_text='Make sure to include timezone', max_length=1000, null=True, verbose_name='meeting times (en)'),
        ),
        migrations.AddField(
            model_name='meeting',
            name='time_description_fr',
            field=models.CharField(blank=True, default='9h à 16h (Atlantique)', help_text='Make sure to include timezone', max_length=1000, null=True, verbose_name='meeting times (fr)'),
        ),
        migrations.AlterField(
            model_name='inviteerole',
            name='category',
            field=models.IntegerField(blank=True, choices=[(1, 'chair'), (2, 'client lead'), (3, 'steering committee member'), (4, 'science lead')], null=True, verbose_name='special category'),
        ),
        migrations.AlterField(
            model_name='process',
            name='editors',
            field=models.ManyToManyField(blank=True, help_text='A list of non-CSAS staff with permissions to edit the process, meetings and documents', related_name='process_editors', to=settings.AUTH_USER_MODEL, verbose_name='process editors'),
        ),
    ]