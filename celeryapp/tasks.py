from celery import shared_task
from time import sleep
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@shared_task()
def run_task(a, b):
    sleep(20)
    return int(a) * int(b)


@shared_task()
def get_log(channel_name, file_name):
    channel_layer = get_channel_layer()

    try:
        with open(file_name) as f:
            f.seek(0, 2)

            while True:
                line = f.readline()

                if line:
                    print(channel_name, line)
                    async_to_sync(channel_layer.send)(
                        channel_name,
                        {
                            "type": "send.message",
                            "message": str(line)
                        }
                    )
                else:
                    sleep(1)
    except Exception as e:
        print(e)
