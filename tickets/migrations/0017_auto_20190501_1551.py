# Generated by Django 2.1.4 on 2019-05-01 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0016_auto_20190501_1346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='app',
            field=models.CharField(blank=True, choices=[('general', 'n/a'), ('camp', 'CAMP db'), ('diets', 'Marine diets'), ('esee', 'ESEE (not part of site)'), ('grais', 'grAIS'), ('herring', 'HerMorrhage'), ('ihub', 'iHub'), ('inventory', 'metadata inventory'), ('masterlist', 'Masterlist'), ('meq', 'Marine environmental quality (MEQ)'), ('oceanography', 'Oceanography'), ('plankton', 'Plankton Net (not part of site)'), ('projects', 'Science project planning'), ('scifi', 'SciFi'), ('shares', 'Gulf Shares'), ('snowcrab', 'Snowcrab'), ('spot', 'G&C App (Spot)'), ('tickets', 'Data Management Ticketing App'), ('travel', 'Travel Plans')], default='general', max_length=25, null=True, verbose_name='application name'),
        ),
    ]