# Generated by Django 3.2.12 on 2022-03-24 14:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fisheriescape', '0039_add_comments_general'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fishery',
            old_name='mitigation_comments',
            new_name='mitigation_comment',
        ),
    ]
