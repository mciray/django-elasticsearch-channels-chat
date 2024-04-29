import json
from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async

class UserStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'user_status'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def user_status(self, event):
        await self.send(text_data=json.dumps({
            'type': 'status',
            'username': event['username'],
            'is_online': event['is_online'],
        }))
class RoomConsumer(WebsocketConsumer):
    def connect(self):
        raw_room_name = self.scope['url_route']['kwargs']['room_name']
        users = raw_room_name.split('_')
        users.sort()
        self.room_name = '_'.join(users)
        self.room_group_name = f'chat_{self.room_name}'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()
       

    def disconnect(self, close_code):
        # Oda grubundan bu kanalı çıkar
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = self.scope['user']

        username = user.username if user.is_authenticated else 'Anonim'

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
              
            }
        )


    def chat_message(self, event):
        message = event['message']

        username = event['username']

        sender = 'self' if self.scope['user'].username == username else 'other'
        
        self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message,
            'username': username,
            'sender': sender
        }))
    
        
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'test'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()
   

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':message
            }
        )

    def chat_message(self, event):
        message = event['message']

        self.send(text_data=json.dumps({
            'type':'chat',
            'message':message
        }))