# Generated by Django 3.2.4 on 2021-10-18 12:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('res', '0016_alter_achievement_detail'),
    ]

    operations = [
        migrations.AddField(
            model_name='achievementcategory',
            name='is_publication',
            field=models.BooleanField(default=False, verbose_name='Is this a category for publications?'),
        ),
        migrations.AlterField(
            model_name='achievement',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='achievements', to='res.achievementcategory', verbose_name='achievement category'),
        ),
        migrations.AlterField(
            model_name='achievement',
            name='date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='date of publication / achievement'),
        ),
        migrations.AlterField(
            model_name='achievement',
            name='publication_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='achievements', to='res.publicationtype', verbose_name='publication type (if applicable)'),
        ),
    ]