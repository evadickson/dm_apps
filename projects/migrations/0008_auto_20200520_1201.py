# Generated by Django 2.2.2 on 2020-05-20 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_auto_20200520_1159'),
    ]

    operations = [
        migrations.AddField(
            model_name='level',
            name='nom',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='name (fr)'),
        ),
        migrations.AlterField(
            model_name='employeetype',
            name='name',
            field=models.CharField(max_length=255, unique=True, verbose_name='name (en)'),
        ),
        migrations.AlterField(
            model_name='employeetype',
            name='nom',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='name (fr)'),
        ),
        migrations.AlterField(
            model_name='level',
            name='name',
            field=models.CharField(max_length=255, unique=True, verbose_name='name (en)'),
        ),
    ]
