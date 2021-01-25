# Generated by Django 3.1.2 on 2021-01-21 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bio_diversity', '0002_auto_20210121_1011'),
    ]

    operations = [
        migrations.CreateModel(
            name='HelpText',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_name', models.CharField(max_length=255)),
                ('eng_text', models.TextField(verbose_name='English text')),
                ('fra_text', models.TextField(blank=True, null=True, verbose_name='French text')),
            ],
            options={
                'ordering': ['field_name'],
            },
        ),
    ]
