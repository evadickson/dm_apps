# Generated by Django 3.2.4 on 2021-10-04 13:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shared_models', '0024_person_expertise'),
        ('csas2', '0042_auto_20211001_1221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='document',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='authors', to='csas2.document', verbose_name='document'),
        ),
        migrations.AlterField(
            model_name='author',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='authorship', to='shared_models.person', verbose_name='person'),
        ),
        migrations.AlterField(
            model_name='csasrequestfile',
            name='caption',
            field=models.CharField(max_length=255, verbose_name='caption'),
        ),
        migrations.AlterField(
            model_name='document',
            name='process',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='csas2.process', verbose_name='process'),
        ),
        migrations.AlterField(
            model_name='documentcost',
            name='description',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='documentcost',
            name='funding_source',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='funding source'),
        ),
        migrations.AlterField(
            model_name='meetingcost',
            name='description',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='meetingcost',
            name='funding_source',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='funding source'),
        ),
        migrations.AlterField(
            model_name='meetingcost',
            name='meeting',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='costs', to='csas2.meeting', verbose_name='meeting'),
        ),
        migrations.AlterField(
            model_name='meetingfile',
            name='caption',
            field=models.CharField(max_length=255, verbose_name='caption'),
        ),
        migrations.CreateModel(
            name='ProcessCost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost_category', models.IntegerField(choices=[(1, 'Translation'), (2, 'Travel'), (3, 'Hospitality'), (4, 'Space rental'), (5, 'Simultaneous translation'), (9, 'Other')], verbose_name='cost category')),
                ('description', models.CharField(blank=True, max_length=1000, null=True, verbose_name='description')),
                ('funding_source', models.CharField(blank=True, max_length=255, null=True, verbose_name='funding source')),
                ('amount', models.FloatField(default=0, verbose_name='amount (CAD)')),
                ('meeting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='costs', to='csas2.process', verbose_name='process')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]