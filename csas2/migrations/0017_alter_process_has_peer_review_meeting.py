# Generated by Django 3.2.10 on 2022-03-01 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('csas2', '0016_auto_20220228_1447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='process',
            name='has_peer_review_meeting',
            field=models.BooleanField(default=False, verbose_name='has peer review meeting?'),
        ),
    ]
