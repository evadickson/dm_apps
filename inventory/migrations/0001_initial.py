# Generated by Django 3.1.2 on 2021-01-25 12:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import dm_apps.custom_widgets
import inventory.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shared_models', '0035_auto_20210114_0553'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='BoundingBox',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('west_bounding', models.FloatField(blank=True, null=True)),
                ('south_bounding', models.FloatField(blank=True, null=True)),
                ('east_bounding', models.FloatField(blank=True, null=True)),
                ('north_bounding', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CharacterSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=25)),
                ('code', models.CharField(blank=True, max_length=25, null=True)),
                ('notes', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ContentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Name (English)')),
                ('english_value', models.CharField(max_length=255, verbose_name='Name (French)')),
                ('french_value', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['title'],
            },
        ),
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
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text_value_eng', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Keyword value (English)')),
                ('text_value_fre', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Keyword value (French)')),
                ('uid', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Unique Identifier')),
                ('concept_scheme', models.CharField(blank=True, max_length=1000, null=True)),
                ('details', models.TextField(blank=True, null=True)),
                ('xml_block', models.TextField(blank=True, null=True)),
                ('is_taxonomic', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['keyword_domain', 'text_value_eng'],
            },
        ),
        migrations.CreateModel(
            name='KeywordDomain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_eng', models.CharField(blank=True, max_length=255, null=True)),
                ('name_fre', models.CharField(blank=True, max_length=255, null=True)),
                ('abbrev', models.CharField(blank=True, max_length=255, null=True)),
                ('url', models.URLField(blank=True, null=True)),
                ('web_services', models.BooleanField()),
                ('xml_block', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location_eng', models.CharField(blank=True, max_length=1000, null=True)),
                ('location_fre', models.CharField(blank=True, max_length=1000, null=True)),
                ('country', models.CharField(choices=[('Canada', 'Canada'), ('United States', 'United States')], max_length=25)),
                ('abbrev_eng', models.CharField(blank=True, max_length=25, null=True)),
                ('abbrev_fre', models.CharField(blank=True, max_length=25, null=True)),
                ('uuid_gcmd', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Maintenance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frequency', models.CharField(max_length=25)),
                ('code', models.CharField(blank=True, max_length=25, null=True)),
                ('notes', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_eng', models.CharField(blank=True, max_length=1000, null=True)),
                ('name_fre', models.CharField(blank=True, max_length=1000, null=True)),
                ('abbrev', models.CharField(blank=True, max_length=255, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('city', models.CharField(blank=True, max_length=255, null=True)),
                ('postal_code', models.CharField(blank=True, max_length=7, null=True)),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='inventory.location')),
            ],
            options={
                'ordering': ['name_eng'],
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='person', serialize=False, to='auth.user')),
                ('full_name', models.CharField(blank=True, max_length=255, null=True)),
                ('position_eng', models.CharField(blank=True, max_length=255, null=True)),
                ('position_fre', models.CharField(blank=True, max_length=255, null=True)),
                ('phone', models.CharField(blank=True, max_length=25, null=True)),
                ('language', models.IntegerField(blank=True, choices=[(1, 'English'), (2, 'French')], null=True, verbose_name='language preference')),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='inventory.organization')),
            ],
            options={
                'ordering': ['user__last_name', 'user__first_name'],
            },
        ),
        migrations.CreateModel(
            name='PersonRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=25)),
                ('code', models.CharField(blank=True, max_length=25, null=True)),
                ('notes', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(blank=True, null=True, unique=True, verbose_name='UUID')),
                ('title_eng', dm_apps.custom_widgets.OracleTextField(verbose_name='Title (English)')),
                ('title_fre', dm_apps.custom_widgets.OracleTextField(blank=True, null=True, verbose_name='Title (French)')),
                ('purpose_eng', dm_apps.custom_widgets.OracleTextField(blank=True, null=True, verbose_name='Purpose (English)')),
                ('purpose_fre', dm_apps.custom_widgets.OracleTextField(blank=True, null=True, verbose_name='Purpose (French)')),
                ('descr_eng', dm_apps.custom_widgets.OracleTextField(blank=True, null=True, verbose_name='Description (English)')),
                ('descr_fre', dm_apps.custom_widgets.OracleTextField(blank=True, null=True, verbose_name='Description (French)')),
                ('time_start_day', models.IntegerField(blank=True, null=True, verbose_name='Start day')),
                ('time_start_month', models.IntegerField(blank=True, null=True, verbose_name='Start month')),
                ('time_start_year', models.IntegerField(blank=True, null=True, verbose_name='Start year')),
                ('time_end_day', models.IntegerField(blank=True, null=True, verbose_name='End day')),
                ('time_end_month', models.IntegerField(blank=True, null=True, verbose_name='End month')),
                ('time_end_year', models.IntegerField(blank=True, null=True, verbose_name='End year')),
                ('sampling_method_eng', models.TextField(blank=True, null=True, verbose_name='Sampling method (English)')),
                ('sampling_method_fre', models.TextField(blank=True, null=True, verbose_name='Sampling method (French)')),
                ('physical_sample_descr_eng', models.TextField(blank=True, null=True, verbose_name='Description of physical samples (English)')),
                ('physical_sample_descr_fre', models.TextField(blank=True, null=True, verbose_name='Description of physical samples (French)')),
                ('resource_constraint_eng', models.TextField(blank=True, null=True, verbose_name='Resource constraint (English)')),
                ('resource_constraint_fre', models.TextField(blank=True, null=True, verbose_name='Resource constraint (French)')),
                ('qc_process_descr_eng', models.TextField(blank=True, null=True, verbose_name='QC process description (English)')),
                ('qc_process_descr_fre', models.TextField(blank=True, null=True, verbose_name='QC process description (French)')),
                ('security_use_limitation_eng', models.CharField(blank=True, max_length=255, null=True, verbose_name='Security use limitation (English)')),
                ('security_use_limitation_fre', models.CharField(blank=True, max_length=255, null=True, verbose_name='Security use limitation (French)')),
                ('storage_envr_notes', models.TextField(blank=True, null=True, verbose_name='Storage notes')),
                ('geo_descr_eng', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Geographic description (English)')),
                ('geo_descr_fre', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Geographic description (French)')),
                ('west_bounding', models.FloatField(blank=True, null=True, verbose_name='West bounding coordinate')),
                ('south_bounding', models.FloatField(blank=True, null=True, verbose_name='South bounding coordinate')),
                ('east_bounding', models.FloatField(blank=True, null=True, verbose_name='East bounding coordinate')),
                ('north_bounding', models.FloatField(blank=True, null=True, verbose_name='North bounding coordinate')),
                ('parameters_collected_eng', models.TextField(blank=True, null=True, verbose_name='Parameters collected (English)')),
                ('parameters_collected_fre', models.TextField(blank=True, null=True, verbose_name='Parameters collected (French)')),
                ('additional_credit', models.TextField(blank=True, null=True)),
                ('analytic_software', models.TextField(blank=True, null=True, verbose_name='Analytic software notes')),
                ('date_verified', models.DateTimeField(blank=True, null=True)),
                ('fgp_url', models.URLField(blank=True, null=True, verbose_name='Link to record on FGP')),
                ('public_url', models.URLField(blank=True, null=True, verbose_name="Link to record on Open Gov't Portal")),
                ('fgp_publication_date', models.DateTimeField(blank=True, null=True, verbose_name='Date published to FGP')),
                ('od_publication_date', models.DateTimeField(blank=True, null=True, verbose_name="Date published to Open Gov't Portal")),
                ('od_release_date', models.DateTimeField(blank=True, null=True, verbose_name="Date released to Open Gov't Portal")),
                ('odi_id', models.CharField(blank=True, max_length=20, null=True, unique=True, verbose_name='ODIP Identifier')),
                ('last_revision_date', models.DateTimeField(blank=True, null=True, verbose_name='Date of last published revision')),
                ('open_data_notes', models.TextField(blank=True, null=True, verbose_name='Open data notes')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='General notes')),
                ('date_last_modified', models.DateTimeField(auto_now=True)),
                ('flagged_4_deletion', models.BooleanField(default=False)),
                ('flagged_4_publication', models.BooleanField(default=False)),
                ('completedness_report', models.TextField(blank=True, null=True, verbose_name='completedness report')),
                ('completedness_rating', models.FloatField(blank=True, null=True, verbose_name='completedness rating')),
                ('translation_needed', models.BooleanField(default=True, verbose_name='translation needed')),
                ('citations2', models.ManyToManyField(blank=True, related_name='resources', to='shared_models.Citation')),
                ('data_char_set', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='inventory.characterset', verbose_name='Data character set')),
                ('distribution_formats', models.ManyToManyField(blank=True, to='inventory.DistributionFormat')),
                ('keywords', models.ManyToManyField(blank=True, related_name='resources', to='inventory.Keyword')),
                ('last_modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('maintenance', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='inventory.maintenance', verbose_name='Maintenance frequency')),
                ('paa_items', models.ManyToManyField(blank=True, to='shared_models.PAAItem', verbose_name='Program Alignment Architecture (PAA) references')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='children', to='inventory.resource', verbose_name='Parent resource')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='ResourceType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=25)),
                ('code', models.CharField(blank=True, max_length=25, null=True)),
                ('notes', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'inventory_resource_type',
            },
        ),
        migrations.CreateModel(
            name='SecurityClassification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=25)),
                ('code', models.CharField(blank=True, max_length=25, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SpatialReferenceSystem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255)),
                ('code', models.CharField(blank=True, max_length=25, null=True)),
                ('codespace', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SpatialRepresentationType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=25)),
                ('code', models.CharField(blank=True, max_length=25, null=True)),
                ('notes', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=25)),
                ('code', models.CharField(blank=True, max_length=25, null=True)),
                ('notes', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='WebService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('protocol', models.CharField(default='ESRI REST: Map Service', max_length=255)),
                ('service_language', models.CharField(choices=[('urn:xml:lang:eng-CAN', 'English'), ('urn:xml:lang:fra-CAN', 'French')], max_length=255)),
                ('url', models.URLField()),
                ('name_eng', models.CharField(max_length=255, verbose_name='Name (English)')),
                ('name_fre', models.CharField(max_length=255, verbose_name='Name (French)')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.contenttype')),
                ('resource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='web_services', to='inventory.resource')),
            ],
        ),
        migrations.CreateModel(
            name='ResourcePerson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', models.TextField(blank=True, null=True)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='resource_people', to='inventory.person')),
                ('resource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resource_people', to='inventory.resource')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='inventory.personrole')),
            ],
            options={
                'db_table': 'inventory_resource_people',
                'ordering': ['role'],
                'unique_together': {('resource', 'person', 'role')},
            },
        ),
        migrations.CreateModel(
            name='ResourceCertification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('certification_date', models.DateTimeField(blank=True, null=True, verbose_name='Date published to FGP')),
                ('notes', models.TextField(null=True)),
                ('certifying_user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('resource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='certification_history', to='inventory.resource')),
            ],
            options={
                'db_table': 'inventory_resource_certification',
                'ordering': ['-certification_date'],
            },
        ),
        migrations.AddField(
            model_name='resource',
            name='people',
            field=models.ManyToManyField(through='inventory.ResourcePerson', to='inventory.Person'),
        ),
        migrations.AddField(
            model_name='resource',
            name='publication_fy',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='shared_models.fiscalyear', verbose_name='FY of latest publication'),
        ),
        migrations.AddField(
            model_name='resource',
            name='resource_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='inventory.resourcetype'),
        ),
        migrations.AddField(
            model_name='resource',
            name='section',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='resources', to='shared_models.section'),
        ),
        migrations.AddField(
            model_name='resource',
            name='security_classification',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='inventory.securityclassification'),
        ),
        migrations.AddField(
            model_name='resource',
            name='spat_ref_system',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='inventory.spatialreferencesystem', verbose_name='Spatial reference system'),
        ),
        migrations.AddField(
            model_name='resource',
            name='spat_representation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='inventory.spatialrepresentationtype', verbose_name='Spatial representation type'),
        ),
        migrations.AddField(
            model_name='resource',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='inventory.status'),
        ),
        migrations.AddField(
            model_name='keyword',
            name='keyword_domain',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='inventory.keyworddomain'),
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=255)),
                ('file', models.FileField(upload_to=inventory.models.file_directory_path)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('resource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='inventory.resource')),
            ],
            options={
                'ordering': ['-date_created'],
            },
        ),
        migrations.CreateModel(
            name='DataResource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('name_eng', models.CharField(max_length=255, verbose_name='Name (English)')),
                ('name_fre', models.CharField(max_length=255, verbose_name='Name (French)')),
                ('protocol', models.CharField(choices=[('HTTP', 'HTTP'), ('HTTPS', 'HTTPS'), ('FTP', 'FTP')], max_length=255)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.contenttype')),
                ('resource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='data_resources', to='inventory.resource')),
            ],
        ),
        migrations.CreateModel(
            name='Correspondence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=255)),
                ('date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('custodian', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='correspondences', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
    ]
