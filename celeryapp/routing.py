from django.urls import path
from celeryapp.consumer import CeleryQuery, AsyncCeleryQuery, GroupCeleryQuery, CeleryTaskLog

celery_websocket_urlpatterns = [
    # path('ws/celery/', CeleryQuery.as_asgi()),
    # path('ws/celery/async/', AsyncCeleryQuery.as_asgi()),
    # path('ws/celery/group/', GroupCeleryQuery.as_asgi()),
    path('ws/celery/log/', CeleryTaskLog.as_asgi()),
]
