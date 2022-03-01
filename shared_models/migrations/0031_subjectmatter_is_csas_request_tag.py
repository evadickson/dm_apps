# Generated by Django 3.2.10 on 2022-02-24 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shared_models', '0030_remove_river_fishing_area_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='subjectmatter',
            name='is_csas_request_tag',
            field=models.BooleanField(default=False, verbose_name='used for CSAS request tagging?'),
        ),
    ]
