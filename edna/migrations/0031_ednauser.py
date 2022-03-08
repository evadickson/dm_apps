# Generated by Django 3.2.10 on 2022-03-01 16:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('edna', '0030_auto_20211201_0930'),
    ]

    operations = [
        migrations.CreateModel(
            name='ednaUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_admin', models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False, verbose_name='app administrator?')),
                ('is_crud_user', models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False, verbose_name='CRUD permissions?')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='edna_user', to=settings.AUTH_USER_MODEL, verbose_name='DM Apps user')),
            ],
            options={
                'ordering': ['-is_admin', 'user__first_name'],
            },
        ),
    ]
