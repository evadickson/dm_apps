# Generated by Django 2.1.4 on 2019-01-18 17:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ihub', '0004_auto_20190117_1548'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='amount_expected',
            field=models.FloatField(blank=True, null=True, verbose_name='How much funding is expected?'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='amount_transferred',
            field=models.FloatField(blank=True, null=True, verbose_name='If yes, how much funding was transferred?'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_entries', to=settings.AUTH_USER_MODEL, verbose_name='created by'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='transferred',
            field=models.NullBooleanField(verbose_name='has any funding been transferred?'),
        ),
    ]
