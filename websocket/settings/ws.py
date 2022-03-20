from decouple import config

REDIS_PASSWORD = config('REDIS_PASSWD')

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [f"redis://:{REDIS_PASSWORD}@127.0.0.1:6379/3"],
        },
    },
}