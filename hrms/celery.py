from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hrms.settings')

app = Celery('basicSetup')
app.conf.enable_utc = False

app.config_from_object(settings, namespace='CELERY')

app.autodiscover_tasks()


app.conf.beat_schedule = {
    'mark-absentees-daily': {
        'task': 'base.tasks.mark_absentees',  # Update to match your actual task path
        'schedule': crontab(minute=50, hour=18),  # Run daily at midnight
    },
}


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")