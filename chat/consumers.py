import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message
class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_group_name = "chat_room"

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

    # chat/consumers.py (Partial code)
async def receive(self, text_data):
    data = json.loads(text_data)
    message = data['message']
    user = self.scope['user']

    # save to datab5ase
    await self.save_message(user, message)

    # send to everyone
    await self.channel_layer.group_send(...)

@database_sync_to_async
def save_message(self, user, message):
    Message.objects.create(user=user, content=message)

    async def chat_message(self, event):
        message = event['message']
        username = event['username'] # This was missing in your screenshot!

        # Send both message and username back to the browser
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))