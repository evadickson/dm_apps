# Generated by Django 3.1.2 on 2021-01-26 01:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shared_models', '0001_initial'),
        ('masterlist', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sector',
            name='region',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='shared_models.region'),
        ),
    ]
