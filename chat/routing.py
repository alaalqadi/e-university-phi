# chat/routing.py
from django.urls import re_path
from chat.consumer import ChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/session_view/(?P<room_name>\w+)/$', ChatConsumer),
]
