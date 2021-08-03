# Generated by Django 3.2.4 on 2021-07-16 11:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scuba', '0005_auto_20210611_1239'),
    ]

    operations = [
        migrations.AddField(
            model_name='dive',
            name='is_training',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False, verbose_name='Was this a training dive?'),
        ),
        migrations.AlterField(
            model_name='dive',
            name='transect',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='dives', to='scuba.transect', verbose_name='transect'),
        ),
    ]
