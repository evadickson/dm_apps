# Generated by Django 3.2.4 on 2021-07-16 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edna', '0014_alter_dnaextract_filter'),
    ]

    operations = [
        migrations.AddField(
            model_name='dnaextract',
            name='extraction_number',
            field=models.CharField(blank=True, max_length=25, null=True, verbose_name='extraction number'),
        ),
    ]
