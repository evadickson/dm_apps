# Generated by Django 3.2.4 on 2021-07-21 14:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('edna', '0020_auto_20210721_1149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pcrassay',
            name='assay',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='pcr_assays', to='edna.pcrbatch', verbose_name='assay'),
        ),
    ]