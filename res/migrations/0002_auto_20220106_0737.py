# Generated by Django 3.2.10 on 2022-01-06 11:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('res', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='achievement',
            name='date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='date of achievement / publication '),
        ),
        migrations.AlterField(
            model_name='achievement',
            name='publication_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='achievements', to='res.publicationtype', verbose_name='achievement sub-category '),
        ),
    ]
