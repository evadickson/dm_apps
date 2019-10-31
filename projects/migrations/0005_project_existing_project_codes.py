# Generated by Django 2.2.2 on 2019-10-30 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shared_models', '0025_region_head'),
        ('projects', '0004_remove_project_is_negotiable'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='existing_project_codes',
            field=models.ManyToManyField(blank=True, null=True, to='shared_models.Project', verbose_name='existing project codes (if known)'),
        ),
    ]
