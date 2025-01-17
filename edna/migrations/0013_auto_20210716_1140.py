# Generated by Django 3.2.4 on 2021-07-16 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edna', '0012_filter_filtration_ipc'),
    ]

    operations = [
        migrations.AddField(
            model_name='dnaextract',
            name='extraction_plate_id',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='extraction plate ID'),
        ),
        migrations.AddField(
            model_name='dnaextract',
            name='extraction_plate_well',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='extraction plate well'),
        ),
        migrations.AlterField(
            model_name='dnaextract',
            name='start_datetime',
            field=models.DateTimeField(verbose_name='extraction date/time'),
        ),
        migrations.AlterField(
            model_name='dnaextract',
            name='storage_location',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='DNA storage location'),
        ),
    ]
