# Generated by Django 2.1.4 on 2019-05-13 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grais', '0029_surface_old_plateheader_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='species',
            name='old_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]