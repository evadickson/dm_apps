# Generated by Django 2.2.2 on 2020-06-22 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0011_auto_20200520_1150'),
    ]

    operations = [
        migrations.CreateModel(
            name='DistributionFormat',
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
        migrations.AddField(
            model_name='resource',
            name='distribution_formats',
            field=models.ManyToManyField(blank=True, to='inventory.DistributionFormat'),
        ),
    ]