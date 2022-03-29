# Generated by Django 3.2.12 on 2022-03-29 13:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shared_models', '0031_subjectmatter_is_csas_request_tag'),
        ('maret', '0015_auto_20220317_1405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='committee',
            name='branch',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='committee_branch', to='shared_models.branch', verbose_name='Lead DFO branch'),
        ),
    ]
