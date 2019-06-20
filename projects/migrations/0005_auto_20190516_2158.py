# Generated by Django 2.1.4 on 2019-05-17 00:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_auto_20190429_1118'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='is_competitive',
            field=models.NullBooleanField(default=False, verbose_name='Is the funding stream for this project competitive (e.g. ACRDP, PARR, SPERA)'),
        ),
        migrations.AddField(
            model_name='project',
            name='is_national',
            field=models.NullBooleanField(default=False, verbose_name='Is this a national project?'),
        ),
        migrations.AddField(
            model_name='project',
            name='is_negotiable',
            field=models.NullBooleanField(default=True, verbose_name='Is this project negotiable?'),
        ),
        migrations.AlterField(
            model_name='project',
            name='end_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='End date of project'),
        ),
        migrations.AlterField(
            model_name='project',
            name='start_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Start date of project'),
        ),
    ]