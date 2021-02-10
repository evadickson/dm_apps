# Generated by Django 3.1.2 on 2020-10-28 13:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shared_models', '0001_initial'),
        ('cruises', '0002_componenttype_instrument_instrumentcomponent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='date_created',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.CreateModel(
            name='CruiseInstruments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cruise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cruise_instruments', to='shared_models.cruise')),
                ('instrument', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cruise_instruments', to='cruises.instrument')),
            ],
        ),
    ]