import json
from time import sleep

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from celery.result import AsyncResult
from .tasks import get_log
from websocket.settings.base import LOGS


class CeleryQuery(WebsocketConsumer):

    def connect(self):
        self.channel_name = 'celery_task'
        self.accept()
        self.send(text_data=json.dumps({
            'message': 'Connection Received!'
        }))

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        if 'initial' in text_data_json:
            print('Received Greeting from client!')
            async_to_sync(self.send(text_data=json.dumps({
                'status': True,
                'message': 'Welcome to use Websocket server, have fun!',
                'result': {}
            })))
            return
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


class AsyncCeleryQuery(AsyncWebsocketConsumer):
    async def connect(self):
        self.channel_name = 'async_celery_task'
        await self.accept()
        await self.send(text_data=json.dumps({
            'message': 'Async Connection Received!'
        }))

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        if 'initial' in text_data_json:
            print('Received Greeting from client!')
            async_to_sync(self.send(text_data=json.dumps({
                'status': True,
                'message': 'Welcome to use Websocket server, have fun!',
                'result': {}
            })))
            return
        task_id = text_data_json['task_id']
        task = AsyncResult(task_id)
        """Have problem when using while loop in async function"""
        while not task.ready():
            content = json.dumps({
                'pending': True,
                'message': 'PENDING'
            })
            async_to_sync(self.send(text_data=content))
            sleep(2)

        content = json.dumps({
            'success': True,
            'message': f'Task{task_id} already finished',
            'result': task.result
        })
        async_to_sync(self.send(text_data=content))

    def send_message(self, event):
        pass


class GroupCeleryQuery(WebsocketConsumer):
    def connect(self):
        data = self.scope

        self.room_group_name = 'celery_group'
        self.channel_name = 'celery_task'

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
        if 'initial' in text_data_json:
            print('Received Greeting from client!')
            message = json.dumps({
                'status': 'CONNECTED',
                'message': 'Welcome to use Websocket server, have fun!',
                'result': {}
            })
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'send.message',
                    'message': message
                })
            return
        task_id = text_data_json['task_id']
        task = AsyncResult(task_id)
        while not task.ready():
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'send.message',
                    'message': json.dumps({
                        'status': 'PENDING',
                        'message': f'Task {task_id} is being processed',
                        'result': {}
                    })
                }
            )
            sleep(1)
        message = json.dumps({
            'status': 'SUCCESS',
            'message': f'Task {task_id} already finished',
            'result': task.result
        })
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'send.message',
                'message': message
            })

    def send_message(self, event):
        self.send(text_data=json.dumps({
            'message': event['message']
        }))


class CeleryTaskLog(WebsocketConsumer):
    def connect(self):
        self.channel_name = 'celery_task_log'
        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        if 'initial' in text_data_json:
            print('Received Greeting from client!')
            message = json.dumps({
                'status': 'CONNECTED',
                'message': 'Welcome to use Websocket server, have fun!',
            })
            self.send(text_data=message)
            return
        task_id = text_data_json['task_id']
        task = AsyncResult(task_id)
        if not task.ready():
            self.result = get_log.delay(self.channel_name, LOGS.get('password'))

        message = json.dumps({
            'status': 'SUCCESS',
            'message': f'Task {task_id} already finished',
            'result': task.result
        })
        self.send(text_data=message)

    def disconnect(self, code):
        self.result.revoke(terminate=True)
        self.send(text_data=json.dumps({
            'status': 'DISCONNECTED',
            'message': f"disconnected: {self.channel_name} :: {self.result.id}",
        }))

    def send_message(self, event):
        self.send(text_data=json.dumps({
            'status': 'SENDING',
            'message': event['message'],
        }))

    @property
    def get_channel_name(self):
        return self.channel_name
