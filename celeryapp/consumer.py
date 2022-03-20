import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from celery.result import AsyncResult


class CeleryQuery(AsyncWebsocketConsumer):
    channel_name = 'celery_task'

    async def connect(self):
        task_id = self.scope['session']['task_id']
        task = AsyncResult(task_id)
        if task.ready():
            content = json.dumps({
                'success': True,
                'message': f'Task{task_id} already finished',
                'result': task.result
            })
            await self.send(text_data={
                'content': content
            })
        else:
            content = json.dumps({
                'pending': True,
            })
            await self.send(text_data={
                'content': content
            })
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        await self.send(json.dumps({
            'message': message
        }))

    async def send_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message']
        }))
