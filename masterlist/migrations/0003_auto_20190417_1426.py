# Generated by Django 2.1.4 on 2019-04-17 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masterlist', '0002_organization_website'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='election_term',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='election term (iHub only)'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='fin',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='FIN (iHub only)'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='name_eng',
            field=models.CharField(max_length=1000, verbose_name='english name'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='next_election',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='next election (iHub only)'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='population_off_reserve',
            field=models.IntegerField(blank=True, null=True, verbose_name='population off reserve (iHub only)'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='population_on_reserve',
            field=models.IntegerField(blank=True, null=True, verbose_name='population on reserve (iHub only)'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='population_other_reserve',
            field=models.IntegerField(blank=True, null=True, verbose_name='population on other reserve (iHub only)'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='website',
            field=models.URLField(blank=True, null=True, verbose_name='website (iHub only)'),
        ),
    ]