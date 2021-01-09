import os

from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'parcer_template_v_2.settings')

app = Celery('parcer_template_v_2')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


app.conf.beat_schedule = {
    # Executes every minute.
    'run-every-minute': {
        'task': 'job_parser.tasks.add',
        'schedule': crontab(),
        'args': (),
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')