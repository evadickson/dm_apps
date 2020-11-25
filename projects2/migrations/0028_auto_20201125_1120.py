# Generated by Django 3.1.2 on 2020-11-25 15:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects2', '0027_auto_20201125_0509'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='milestone',
            options={'ordering': ['project_year', 'target_date', 'name']},
        ),
        migrations.AlterModelOptions(
            name='referencematerial',
            options={'ordering': ['region', 'name']},
        ),
        migrations.RenameField(
            model_name='referencematerial',
            old_name='file',
            new_name='file_en',
        ),
    ]
