# Generated by Django 2.0.4 on 2018-09-10 14:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('herring', '0020_auto_20180910_1113'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fishdetail',
            old_name='lab_sampler2',
            new_name='lab_sampler',
        ),
        migrations.RemoveField(
            model_name='fishdetail',
            name='ager',
        ),
        migrations.RemoveField(
            model_name='fishdetail',
            name='detail_sampler',
        ),
    ]