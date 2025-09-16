import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from .models import Message

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.other_user_id = self.scope["url_route"]["kwargs"]["user_id"]
        self.room_name = f"chat_{min(self.user.id, self.other_user_id)}_{max(self.user.id, self.other_user_id)}"

        # Room ga ulanish
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        text = data["text"]

        # Bazaga saqlash
        sender = self.user
        receiver = await self.get_user(self.other_user_id)
        msg = await self.create_message(sender, receiver, text)

        # Barcha userlarga yuborish
        await self.channel_layer.group_send(
            self.room_name,
            {
                "type": "chat_message",
                "sender": sender.username,
                "text": msg.text,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "sender": event["sender"],
            "text": event["text"],
        }))

    @staticmethod
    async def get_user(user_id):
        return await User.objects.aget(id=user_id)

    @staticmethod
    async def create_message(sender, receiver, text):
        return await Message.objects.acreate(sender=sender, receiver=receiver, text=text)
