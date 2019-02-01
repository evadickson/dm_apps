# Generated by Django 2.1.4 on 2019-01-31 14:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('scifi', '0023_auto_20190131_0854'),
    ]

    operations = [
        migrations.AddField(
            model_name='allotmentcode',
            name='category',
            field=models.CharField(choices=[('salary', 'Salary'), ('capital', 'Capital'), ('om', 'O&M'), ('gc', 'G&C'), ('other', 'Other')], default='other', max_length=25),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='creation_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]