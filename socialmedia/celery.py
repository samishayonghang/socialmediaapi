import os
from celery import Celery
from django.conf import settings

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socialmedia.settings')

# Create the Celery app
app = Celery('socialmedia')

# Load config from Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Update Celery settings
app.conf.update(
    broker_url=os.getenv('CELERY_BROKER_URL'),  # Use 'redis://' for internal
    accept_content=['json'],
    task_serializer='json',
    task_default_queue='default',
    task_create_missing_queues=True,
    worker_pool='solo',  # Good for Windows/local dev; use 'prefork' in prod Linux
)

# Autodiscover tasks from your apps
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
