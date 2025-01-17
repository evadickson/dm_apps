from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

# set the default Django settings module for the 'celery' program.

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dm_apps.settings')

app = Celery('dm_apps')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# see https://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html as a reference
app.conf.beat_schedule = {
    'run_chunk_pageviews': {
        'task': 'chunk_pageviews',
        'schedule': 60 * 60,  # Execute every 5 seconds
    },
}
