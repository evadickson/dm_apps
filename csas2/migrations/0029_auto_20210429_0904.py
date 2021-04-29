# Generated by Django 3.2 on 2021-04-29 12:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('csas2', '0028_auto_20210429_0844'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='end_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='anticipated end date'),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='location',
            field=models.CharField(blank=True, help_text='City, State/Province, Country or Virtual', max_length=1000, null=True, verbose_name='location'),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='start_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='initial activity date'),
        ),
        migrations.AlterField(
            model_name='termsofreference',
            name='meeting',
            field=models.OneToOneField(blank=True, help_text='The ToR will pull several fields from the linked meeting (e.g., dates, chair, location, ...)', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='tor', to='csas2.meeting', verbose_name='Linked to which meeting?'),
        ),
    ]
