# Generated by Django 3.2.10 on 2022-01-26 14:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ppt', '0023_alter_dma_storage_solution_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='ppt.activity', verbose_name='parent activity'),
        ),
    ]