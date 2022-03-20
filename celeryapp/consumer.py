import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from celery.result import AsyncResult


class CeleryQuery(WebsocketConsumer):
    channel_name = 'celery_task'

    def connect(self):
        self.accept()
        task_id = self.scope['session']
        task = AsyncResult(task_id)
        if task.ready():
            content = json.dumps({
                'success': True,
                'message': f'Task{task_id} already finished',
                'result': task.result
            })
            self.send(text_data=content)
        else:
            content = json.dumps({
                'pending': True,
            })
            self.send(text_data=content)

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        self.send(json.dumps({
            'message': message
        }))

    def send_message(self, event):
        self.send(text_data=json.dumps({
            'message': event['message']
        }))
