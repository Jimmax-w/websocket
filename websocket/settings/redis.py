# Configure Redis as Django Cache System
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": "Aa123456"
        },
        "KEY_PREFIX": "default"
    },
    'session': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/2',
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": "Aa123456"
        },
        "KEY_PREFIX": "session"
    }
}
# Enable Cache and write to DB
SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
SESSION_CACHE_ALIAS = "session"

# Default is False, Session not expire when close browser.
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# Redis only for cache, ignore exceptions when Redis is down.
DJANGO_REDIS_IGNORE_EXCEPTIONS = True
