# Generated by Django 3.1.2 on 2021-01-13 00:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects2', '0011_collaboration_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collaboration',
            name='amount',
            field=models.FloatField(blank=True, null=True, verbose_name='G&C amount (CAD)'),
        ),
    ]
