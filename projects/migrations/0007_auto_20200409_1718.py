# Generated by Django 2.2.2 on 2020-04-09 20:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_auto_20200409_1717'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fundingsource',
            options={'ordering': ['funding_source_type', 'name']},
        ),
        migrations.AlterUniqueTogether(
            name='fundingsource',
            unique_together={('funding_source_type', 'name')},
        ),
    ]
