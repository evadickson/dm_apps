# Generated by Django 3.2.10 on 2021-12-22 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('csas2', '0008_torreviewer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='torreviewer',
            name='status_date',
        ),
        migrations.AddField(
            model_name='torreviewer',
            name='decision_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='date'),
        ),
        migrations.AlterField(
            model_name='invitee',
            name='status',
            field=models.IntegerField(choices=[(0, 'Invited'), (1, 'Accepted'), (2, 'Declined'), (3, 'Tentative'), (4, 'Proposed')], default=9, verbose_name='status'),
        ),
        migrations.AlterField(
            model_name='termsofreference',
            name='posting_request_date',
            field=models.DateTimeField(blank=True, editable=False, null=True, verbose_name='Date of posting request'),
        ),
        migrations.AlterField(
            model_name='torreviewer',
            name='comments',
            field=models.TextField(null=True, verbose_name='comments'),
        ),
        migrations.AlterField(
            model_name='torreviewer',
            name='status',
            field=models.IntegerField(choices=[(10, 'Draft'), (20, 'Queued'), (30, 'Pending'), (40, 'Complete')], default=10, verbose_name='status'),
        ),
    ]