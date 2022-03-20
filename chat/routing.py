from django.urls import path
from chat.consumer import AsyncGroupChatConsumer
websocket_urlpatterns = [
    path('ws/socket', AsyncGroupChatConsumer),
]
