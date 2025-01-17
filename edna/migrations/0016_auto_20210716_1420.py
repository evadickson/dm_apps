# Generated by Django 3.2.4 on 2021-07-16 17:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('edna', '0015_dnaextract_extraction_number'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pcr',
            options={'ordering': ['id']},
        ),
        migrations.RemoveField(
            model_name='pcr',
            name='pcr_number_prefix',
        ),
        migrations.RemoveField(
            model_name='pcr',
            name='pcr_number_suffix',
        ),
        migrations.AlterField(
            model_name='dnaextract',
            name='filter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='extracts', to='edna.filter', verbose_name='filter ID'),
        ),
        migrations.AlterField(
            model_name='filter',
            name='sample',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='filters', to='edna.sample', verbose_name='sample ID'),
        ),
        migrations.AlterField(
            model_name='pcr',
            name='extract',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='pcrs', to='edna.dnaextract', verbose_name='extraction ID'),
        ),
        migrations.AlterField(
            model_name='pcr',
            name='plate_id',
            field=models.CharField(blank=True, max_length=25, null=True, verbose_name='qPCR plate ID'),
        ),
        migrations.AlterField(
            model_name='pcr',
            name='start_datetime',
            field=models.DateTimeField(verbose_name='qPCR date/time'),
        ),
    ]
