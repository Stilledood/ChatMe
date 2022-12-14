from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/messenger/chat_room/(?P<room_name>\w+)/$",consumers.ChatConsumer.as_asgi()),
    re_path(r"ws/messenger/private_room/(?P<pk>[0-9A-Fa-f-]+)/$",consumers.DirectChatConsumer.as_asgi())
]