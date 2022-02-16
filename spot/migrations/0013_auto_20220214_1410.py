# Generated by Django 3.1.2 on 2022-02-14 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spot', '0012_auto_20220210_0801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='data_quality_check',
            field=models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='Was sample data quality check complete?'),
        ),
        migrations.AlterField(
            model_name='data',
            name='sample_entered_database',
            field=models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='Was sample collection data entered into database(s)?'),
        ),
        migrations.AlterField(
            model_name='fundingyears',
            name='agreement_cost',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Annual Agreement Cost'),
        ),
        migrations.AlterField(
            model_name='fundingyears',
            name='project_cost',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Annual Project Cost'),
        ),
        migrations.AlterField(
            model_name='methoddocument',
            name='publication_year',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='year of publication'),
        ),
        migrations.AlterField(
            model_name='methoddocument',
            name='reference_number',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='reference number'),
        ),
        migrations.AlterField(
            model_name='methoddocument',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='objective',
            name='dfo_report',
            field=models.TextField(blank=True, max_length=1000, null=True, verbose_name='Products/Reports to Provide DFO'),
        ),
        migrations.AlterField(
            model_name='objective',
            name='element_title',
            field=models.TextField(blank=True, max_length=1000, null=True, verbose_name='Element Title'),
        ),
        migrations.AlterField(
            model_name='objective',
            name='expected_results',
            field=models.TextField(blank=True, max_length=1000, null=True, verbose_name='Expected Result(s)'),
        ),
        migrations.AlterField(
            model_name='objective',
            name='outcome_met',
            field=models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='Was the Sampling outcome met?'),
        ),
        migrations.AlterField(
            model_name='objective',
            name='pst_requirement',
            field=models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='PST Requirement Identified?'),
        ),
        migrations.AlterField(
            model_name='objective',
            name='sil_requirement',
            field=models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='SIL Requirement'),
        ),
        migrations.AlterField(
            model_name='person',
            name='section',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Section'),
        ),
        migrations.AlterField(
            model_name='project',
            name='agreement_number',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Agreement Number'),
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.TextField(blank=True, max_length=1000, null=True, verbose_name='Project Name'),
        ),
        migrations.AlterField(
            model_name='reportoutcome',
            name='outcome_delivered',
            field=models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='Was the outcome deliverable met?'),
        ),
        migrations.AlterField(
            model_name='reportoutcome',
            name='unique_objective_number',
            field=models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='Unique Objective Number'),
        ),
        migrations.AlterField(
            model_name='reports',
            name='published',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Was this report Published?'),
        ),
        migrations.AlterField(
            model_name='river',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='sampleoutcome',
            name='outcome_delivered',
            field=models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='Was the Sampling Outcome Met?'),
        ),
        migrations.AlterField(
            model_name='sampleoutcome',
            name='outcome_report_delivered',
            field=models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='Were outcome reports delivered?'),
        ),
        migrations.AlterField(
            model_name='sampleoutcome',
            name='unique_objective_number',
            field=models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='Unique Objective Number'),
        ),
    ]