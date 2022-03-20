import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'websocket.settings.develop')
app = Celery('websocket')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.enable_utc = True
app.conf.timezone = 'Asia/Shanghai'
