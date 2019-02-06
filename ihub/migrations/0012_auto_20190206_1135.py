# Generated by Django 2.1.4 on 2019-02-06 15:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ihub', '0011_auto_20190206_1131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='entry_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='entries', to='ihub.EntryType'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='funding_purpose',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='entries', to='ihub.FundingPurpose', verbose_name='funding purpose'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='entries', to='ihub.Organization'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='entries', to='ihub.Region'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='sector',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='entries', to='ihub.Sector'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='status',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='entries', to='ihub.Status', verbose_name='status'),
        ),
    ]
