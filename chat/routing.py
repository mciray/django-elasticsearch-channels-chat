from django.urls import re_path,path
from . import consumers

websocket_urlpatterns = [
    path('ws/socket-server/', consumers.ChatConsumer.as_asgi()),
    path('ws/socket-server/<str:room_name>/', consumers.RoomConsumer.as_asgi()),
]