from channels.auth import AuthMiddlewareStack
from channels.sessions import SessionMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing
import celeryapp.routing

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(SessionMiddlewareStack(
        URLRouter(
            celeryapp.routing.celery_websocket_urlpatterns
        )
    ))
})
