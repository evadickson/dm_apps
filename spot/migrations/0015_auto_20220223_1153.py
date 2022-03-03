# Generated by Django 3.1.2 on 2022-02-23 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spot', '0014_auto_20220216_2149'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='objective',
            name='outcome_met',
        ),
        migrations.AlterField(
            model_name='methoddocument',
            name='authors',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Author'),
        ),
        migrations.AlterField(
            model_name='methoddocument',
            name='document_link',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Document Link'),
        ),
        migrations.AlterField(
            model_name='methoddocument',
            name='method_document_type',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Method Document Type'),
        ),
        migrations.AlterField(
            model_name='methoddocument',
            name='publication_year',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Year of Publication'),
        ),
        migrations.AlterField(
            model_name='methoddocument',
            name='reference_number',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Reference Number'),
        ),
        migrations.AlterField(
            model_name='methoddocument',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Title'),
        ),
        migrations.RemoveField(
            model_name='project',
            name='cu_name',
        ),
        migrations.AddField(
            model_name='project',
            name='cu_name',
            field=models.ManyToManyField(blank=True, null=True, to='spot.CUName', verbose_name='CU Name'),
        ),
    ]
