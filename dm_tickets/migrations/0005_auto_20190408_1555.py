# Generated by Django 2.1.4 on 2019-04-08 18:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dm_tickets', '0004_auto_20190408_1306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='section',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='shared_models.Section'),
        ),
    ]