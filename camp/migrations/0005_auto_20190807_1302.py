# Generated by Django 2.2.2 on 2019-08-07 16:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('camp', '0004_auto_20190807_1301'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='site',
            options={'ordering': ['province', 'site']},
        ),
        migrations.RenameField(
            model_name='site',
            old_name='province2',
            new_name='province',
        ),
    ]
