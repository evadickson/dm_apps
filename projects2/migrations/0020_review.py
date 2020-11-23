# Generated by Django 3.1.2 on 2020-11-23 17:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects2', '0019_auto_20201119_0851'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('general_comment', models.TextField(blank=True, null=True, verbose_name='general comments')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('last_modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='last_mod_by_projects_review', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
                ('project_year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='projects2.projectyear')),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
    ]
