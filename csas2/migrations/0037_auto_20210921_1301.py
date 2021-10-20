# Generated by Django 3.2.4 on 2021-09-21 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('csas2', '0036_auto_20210921_0846'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='csasrequest',
            name='had_assistance',
        ),
        migrations.AddField(
            model_name='csasrequestfile',
            name='is_approval',
            field=models.BooleanField(default=False, verbose_name='is this file an approval for this request?'),
        ),
        migrations.AlterField(
            model_name='csasrequest',
            name='assistance_text',
            field=models.TextField(blank=True, null=True, verbose_name='From whom in Science have you had assistance in developing the question/request (CSAS and/or DFO science staff)'),
        ),
        migrations.AlterField(
            model_name='csasrequest',
            name='is_multiregional',
            field=models.IntegerField(blank=True, choices=[(None, 'Unsure'), (1, 'Yes'), (0, 'No')], default=False, help_text='e.g., frameworks, tools, issues and/or aquatic species widely distributed throughout more than one region', null=True, verbose_name='Could the advice provided potentially be applicable to other regions and/or sectors?'),
        ),
        migrations.AlterField(
            model_name='csasrequest',
            name='rationale_for_timeline',
            field=models.TextField(blank=True, help_text='e.g., COSEWIC or consultation meetings, Environmental Assessments, legal or regulatory requirement, Treaty obligation, international commitments, etc). Please elaborate and provide anticipatory dates', null=True, verbose_name='Rationale for deadline?'),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='time_description_fr',
            field=models.CharField(blank=True, help_text='e.g.: 9h à 16h (Atlantique)', max_length=1000, null=True, verbose_name='description of meeting times (fr)'),
        ),
    ]