# Generated by Django 3.2.4 on 2021-07-21 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edna', '0022_alter_pcrassay_assay'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pcrassay',
            name='result',
            field=models.IntegerField(choices=[(8, 'in progress'), (1, 'positive'), (0, 'negative'), (9, 'undetermined')], default=8, editable=False, verbose_name='result'),
        ),
    ]