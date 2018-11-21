# Generated by Django 2.0.4 on 2018-11-19 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('camp', '0017_auto_20181119_1546'),
    ]

    operations = [
        migrations.AddField(
            model_name='sample',
            name='timezone',
            field=models.CharField(blank=True, choices=[('AST', 'AST'), ('ADT', 'ADT'), ('UTC', 'UTC')], max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='sample',
            name='sample_end_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='End date / time (yyyy-mm-dd hh:mm:ss)'),
        ),
        migrations.AlterField(
            model_name='sample',
            name='sample_start_date',
            field=models.DateTimeField(verbose_name='Start date / time (yyyy-mm-dd hh:mm:ss)'),
        ),
        migrations.AlterField(
            model_name='sample',
            name='tide_state',
            field=models.CharField(blank=True, choices=[('h', 'High'), ('m', 'Mid'), ('l', 'Low')], max_length=5, null=True),
        ),
    ]