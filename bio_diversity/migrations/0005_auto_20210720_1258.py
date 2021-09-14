# Generated by Django 3.2.4 on 2021-07-20 15:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bio_diversity', '0004_alter_envtreatment_unique_together'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='releasesitecode',
            options={'ordering': ['name']},
        ),
        migrations.AddField(
            model_name='tributary',
            name='subr_id',
            field=models.ForeignKey(blank=True, db_column='SUBRIVER_ID', null=True, on_delete=django.db.models.deletion.CASCADE, to='bio_diversity.subrivercode', verbose_name='Subriver'),
        ),
        migrations.AlterField(
            model_name='location',
            name='end_lat',
            field=models.DecimalField(blank=True, db_column='END_LATITUDE', decimal_places=6, max_digits=8, null=True, verbose_name='End Latitude'),
        ),
        migrations.AlterField(
            model_name='location',
            name='end_lon',
            field=models.DecimalField(blank=True, db_column='END_LONGITUDE', decimal_places=6, max_digits=9, null=True, verbose_name='End Longitude'),
        ),
        migrations.AlterField(
            model_name='location',
            name='loc_lat',
            field=models.DecimalField(blank=True, db_column='LATITUDE', decimal_places=6, max_digits=8, null=True, verbose_name='Latitude'),
        ),
        migrations.AlterField(
            model_name='location',
            name='loc_lon',
            field=models.DecimalField(blank=True, db_column='LONGITUDE', decimal_places=6, max_digits=9, null=True, verbose_name='Longitude'),
        ),
        migrations.AlterField(
            model_name='releasesitecode',
            name='max_lat',
            field=models.DecimalField(blank=True, db_column='MAX_LATITUDE', decimal_places=6, max_digits=8, null=True, verbose_name='Max Latitude'),
        ),
        migrations.AlterField(
            model_name='releasesitecode',
            name='max_lon',
            field=models.DecimalField(blank=True, db_column='MAX_LONGITUDE', decimal_places=6, max_digits=9, null=True, verbose_name='Max Longitude'),
        ),
        migrations.AlterField(
            model_name='releasesitecode',
            name='min_lat',
            field=models.DecimalField(blank=True, db_column='MIN_LATITUDE', decimal_places=6, max_digits=8, null=True, verbose_name='Min Latitude'),
        ),
        migrations.AlterField(
            model_name='releasesitecode',
            name='min_lon',
            field=models.DecimalField(blank=True, db_column='MIN_LONGITUDE', decimal_places=6, max_digits=9, null=True, verbose_name='Min Longitude'),
        ),
        migrations.AlterField(
            model_name='subrivercode',
            name='name',
            field=models.CharField(max_length=255, verbose_name='name (en)'),
        ),
        migrations.AlterField(
            model_name='tributary',
            name='name',
            field=models.CharField(max_length=255, verbose_name='name (en)'),
        ),
        migrations.AlterUniqueTogether(
            name='subrivercode',
            unique_together={('name', 'rive_id', 'trib_id')},
        ),
        migrations.AlterUniqueTogether(
            name='tributary',
            unique_together={('name', 'rive_id', 'subr_id')},
        ),
    ]