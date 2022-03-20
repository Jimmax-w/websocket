import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer


class SingleChatConsumer(WebsocketConsumer):
    def connect(self):
        print('--->:' + str(self.channel_layer))
        self.accept()

    def disconnect(self, code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = 'Devops Coffee：' + text_data_json['message']

        self.send(text_data=json.dumps({
            'message': message
        }))


class SyncGroupChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'sync_devops_coffee'
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = 'Devops Coffee：' + text_data_json['message']
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def chat_message(self, event):
        message = 'Devops Coffee：' + event['message']
        self.send(text_data=json.dumps({
            'message': message
        }))


class AsyncGroupChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'async_devops_coffee'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = 'Devops Coffee：' + text_data_json['message']

        await self.channel_layer.group_add(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        message = 'Devops Coffee：' + event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))
