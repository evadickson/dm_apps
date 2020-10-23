# Generated by Django 2.2.13 on 2020-10-23 17:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cruises', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComponentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='name (en)')),
                ('nom', models.CharField(blank=True, max_length=255, null=True, verbose_name='name (fr)')),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Instrument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='name')),
                ('notes', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='InstrumentComponent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_number', models.CharField(blank=True, max_length=1000, null=True, verbose_name='model number')),
                ('serial_number', models.CharField(blank=True, max_length=1000, null=True, verbose_name='serial number')),
                ('notes', models.TextField(blank=True, null=True)),
                ('component_type', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='components', to='cruises.ComponentType', verbose_name='component type')),
                ('instrument', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='components', to='cruises.Instrument')),
            ],
        ),
    ]
