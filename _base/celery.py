import os

from decouple import config

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '_base.settings')

app = Celery('core', broker=config('RABBITMQ_URL', default='pyamqp://guest@localhost//'))

app.config_from_object('django.conf:settings', namespace='CORE')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'populate_funds': {
        'task': 'fund.tasks.populator.populate_funds',
        'schedule': 10,
        'options': {
            'queue': 'fund',
            'expires': 10
        },
    },
    'populate_funds_detail': {
        'task': 'fund.tasks.populator.populate_funds_detail',
        'schedule': 10,
        'options': {
            'queue': 'fund',
            'expires': 10
        },
    },
}
