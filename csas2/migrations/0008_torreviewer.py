# Generated by Django 3.2.10 on 2021-12-20 14:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('csas2', '0007_alter_termsofreference_is_complete'),
    ]

    operations = [
        migrations.CreateModel(
            name='ToRReviewer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('order', models.IntegerField(null=True, verbose_name='process order')),
                ('decision', models.IntegerField(blank=True, choices=[(1, 'Accept'), (2, 'Request changes')], null=True, verbose_name='decision')),
                ('comments', models.TextField(null=True, verbose_name='Comments')),
                ('status', models.IntegerField(choices=[(10, 'Draft'), (20, 'Queued'), (30, 'Pending'), (40, 'Complete')], default=10, verbose_name='review status')),
                ('status_date', models.DateTimeField(blank=True, null=True, verbose_name='status date')),
                ('created_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='torreviewer_created_by', to=settings.AUTH_USER_MODEL)),
                ('tor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviewers', to='csas2.termsofreference')),
                ('updated_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='torreviewer_updated_by', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='tor_reviews', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'ToR reviewer',
                'ordering': ['tor', 'order'],
                'unique_together': {('tor', 'user')},
            },
        ),
    ]