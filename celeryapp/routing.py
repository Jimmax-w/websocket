from django.urls import path
from celeryapp.consumer import CeleryQuery
celery_websocket_urlpatterns = [
    path('ws/celery/', CeleryQuery.as_asgi()),
]
