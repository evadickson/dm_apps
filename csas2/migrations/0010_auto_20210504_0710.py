# Generated by Django 3.2 on 2021-05-04 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('csas2', '0009_auto_20210504_0705'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meeting',
            name='type',
        ),
        migrations.AddField(
            model_name='meeting',
            name='is_planning',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False, verbose_name='Is this a planning meeting?'),
        ),
        migrations.AddField(
            model_name='meeting',
            name='name',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='title (en)'),
        ),
        migrations.AddField(
            model_name='meeting',
            name='nom',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='title (fr)'),
        ),
    ]
