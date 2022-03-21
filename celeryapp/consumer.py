import json
from time import sleep

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from celery.result import AsyncResult


class CeleryQuery(WebsocketConsumer):

    def connect(self):
        self.channel_name = 'celery_task'
        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        task_id = text_data_json['task_id']
        task = AsyncResult(task_id)
        while not task.ready():
            content = json.dumps({
                'pending': True,
                'message': 'PENDING'
            })
            self.send(text_data=content)
            sleep(2)

        content = json.dumps({
            'success': True,
            'message': f'Task{task_id} already finished',
            'result': task.result
        })
        self.send(text_data=content)

    def send_message(self, event):
        task_id = self.scope['session']
        pass
