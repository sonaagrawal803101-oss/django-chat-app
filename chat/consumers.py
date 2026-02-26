import json
from channels.generic.websocket import AsyncWebsocketConsumer

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

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        # Get the username from the session scope
        username = self.scope["user"].username 

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username, # Sending username to the group
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username'] # This was missing in your screenshot!

        # Send both message and username back to the browser
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))