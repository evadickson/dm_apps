# Generated by Django 2.2.2 on 2019-10-11 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0005_auto_20191011_1057'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='approver_approval_status',
            field=models.IntegerField(blank=True, choices=[(0, 'Pending'), (1, 'Approved'), (2, 'Denied')], default=1, null=True, verbose_name='expenditure initiation approval status'),
        ),
        migrations.AddField(
            model_name='event',
            name='recommender_1_approval_status',
            field=models.IntegerField(blank=True, choices=[(0, 'Pending'), (1, 'Approved'), (2, 'Denied')], default=1, null=True, verbose_name='recommender 1 approval status'),
        ),
        migrations.AddField(
            model_name='event',
            name='recommender_2_approval_status',
            field=models.IntegerField(blank=True, choices=[(0, 'Pending'), (1, 'Approved'), (2, 'Denied')], default=1, null=True, verbose_name='recommender 2 approval status'),
        ),
        migrations.AddField(
            model_name='event',
            name='recommender_3_approval_status',
            field=models.IntegerField(blank=True, choices=[(0, 'Pending'), (1, 'Approved'), (2, 'Denied')], default=1, null=True, verbose_name='recommender 3 approval status'),
        ),
    ]
