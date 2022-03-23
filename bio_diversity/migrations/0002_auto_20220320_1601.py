# Generated by Django 3.2.12 on 2022-03-20 19:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bio_diversity', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='anidetailxref',
            name='final_contx_flag',
        ),
        migrations.AlterUniqueTogether(
            name='groupdet',
            unique_together={('anix_id', 'anidc_id', 'adsc_id', 'frm_grp_id', 'detail_date')},
        ),
        migrations.AlterUniqueTogether(
            name='individualdet',
            unique_together={('anix_id', 'anidc_id', 'adsc_id', 'detail_date')},
        ),
        migrations.AlterUniqueTogether(
            name='sampledet',
            unique_together={('samp_id', 'anidc_id', 'adsc_id', 'detail_date')},
        ),
    ]