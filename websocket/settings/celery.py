# Celery Settings
from decouple import config

# Configure Redis as Django Cache System
REDIS_PASSWORD = config('REDIS_PASSWD')

CELERY_BROKER_URL = f'redis://:{REDIS_PASSWORD}@127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = "django-db"
# CELERY_RESULT_BACKEND = 'redis://:Aa123456@127.0.0.1:6379/3'
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_ENABLE_UTC = False
# celery內容等訊息的格式設定，預設json
CELERY_ACCEPT_CONTENT = ['application/json', ]
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_TIME_LIMIT = 60 * 60
# 每個worker執行了多少任務就會死掉，預設是無限的,建議設置，否則有可能導致內存泄漏風險。
CELERY_WORKER_MAX_TASKS_PER_CHILD = 200
# CELERY_IMPORTS = {
    # "apps.sccm_bios.task",
# }
# Set django_celery_beat as celery beat scheduler
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
