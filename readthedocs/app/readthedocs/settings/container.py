"""Containerized environment settings."""
from __future__ import absolute_import
import os

from .base import CommunityBaseSettings


_redis_host = os.getenv('REDIS_HOST', 'redis')
_redis_port = os.getenv('REDIS_PORT', '6379')
_redis_db = os.getenv('REDIS_DB', '0')

class ContainerSettings(CommunityBaseSettings):
    """Settings for containerized environment"""

    DEBUG = os.getenv('RTD_DEBUG', 'false').lower() == 'true'

    SITE_ROOT = '/app'

    # Set this to the root domain where this RTD installation will be running
    PRODUCTION_DOMAIN = os.getenv('RTD_PRODUCTION_DOMAIN', 'localhost:8000')
    PUBLIC_DOMAIN = os.getenv('RTD_PUBLIC_DOMAIN', PRODUCTION_DOMAIN)
    USE_SUBDOMAIN = os.getenv('RTD_USE_SUBDOMAIN', 'false').lower() == 'true'

    # TODO: WEBSOCKET_HOST = 'localhost:8088'

    # Email
    DEFAULT_FROM_EMAIL = 'no-reply@{}'.format(PRODUCTION_DOMAIN)

    # Cookies
    SESSION_COOKIE_DOMAIN = PRODUCTION_DOMAIN

    AUTHENTICATION_BACKENDS = CommunityBaseSettings.AUTHENTICATION_BACKENDS + ('guardian.backends.ObjectPermissionBackend', )

    # Elasticsearch
    if os.getenv('RTD_HAS_ELASTICSEARCH', 'false').lower() == 'true':
        @property
        def ES_HOSTS(self):  # noqa
            return [
                '{0}:{1}'.format(
                    os.getenv('ELASTICSEARCH_HOST', 'elasticsearch'),
                    os.getenv('ELASTICSEARCH_PORT', '9200')
                )
            ]

    @property
    def DATABASES(self):  # noqa
        if os.getenv('RTD_HAS_DATABASE', 'false').lower() == 'true':
            return {
                'default': {
                    'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.postgresql_psycopg2'),
                    'NAME': os.getenv('DB_NAME', 'readthedocs'),
                    'USER': os.getenv('DB_USER', 'rtd'),
                    'PASSWORD': os.getenv('DB_PASS', 'rtd'),
                    'HOST': os.getenv('DB_HOST', 'database'),
                    'PORT': os.getenv('DB_PORT', 5432),
                }
            }
        else:
            return {
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': os.path.join(self.SITE_ROOT, 'dev.db'),
                }
            }

    SLUMBER_USERNAME = os.getenv('RTD_SLUMBER_USERNAME', 'slumber')
    SLUMBER_PASSWORD = os.getenv('RTD_SLUMBER_PASSWORD', 'slumber')
    SLUMBER_API_HOST = os.getenv('RTD_SLUMBER_API_HOST', 'http://localhost:8000')
    SLUMBER_EMAIL    = os.getenv('RTD_SLUMBER_EMAIL', '{0}@localhost'.format(SLUMBER_USERNAME))

    @property
    def CACHE(self):  # noqa
        if os.getenv('RTD_USE_REDIS_FOR_CACHE', 'false').lower() == 'true':
            return {
                'default': {
                    'BACKEND': 'redis_cache.RedisCache',
                    'LOCATION': 'redis://{0}:{1}/{2}'.format(_redis_host, _redis_port, _redis_db),
                    'OPTIONS': {
                        'PARSER_CLASS': 'redis.connection.HiredisParser',
                        },
                },
            }
        else:
            return {
                'default': {
                    'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
                    'PREFIX': 'docs',
                }
            }

    BROKER_URL = 'redis://{0}:{1}/{2}'.format(_redis_host, _redis_port, _redis_db)
    CELERY_RESULT_BACKEND = 'redis://{0}:{1}/{2}'.format(_redis_host, _redis_port, _redis_db)
    CELERY_RESULT_SERIALIZER = 'json'

    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    FILE_SYNCER = 'readthedocs.builds.syncers.LocalSyncer'

    # Users
    ADMIN_USERNAME = os.getenv('RTD_ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD = os.getenv('RTD_ADMIN_PASSWORD', 'admin')
    ADMIN_EMAIL    = os.getenv('RTD_ADMIN_EMAIL', '{0}@{1}'.format(ADMIN_USERNAME, '.'.join(PRODUCTION_DOMAIN.split('.')[-2:])))

    ADMINS = ( (os.getenv('RTD_ADMIN_NAME', 'RTD Admin'), ADMIN_EMAIL), )

    GLOBAL_ANALYTICS_CODE = os.getenv('RTD_GLOBAL_ANALYTICS_CODE', '')

    # Turn off email verification
    ACCOUNT_EMAIL_VERIFICATION = os.getenv('RTD_ACCOUNT_EMAIL_VERIFICATION', 'none')

    # Enable private Git repositories
    ALLOW_PRIVATE_REPOS = os.getenv('RTD_ALLOW_PRIVATE_REPOS', 'false').lower() == 'true'
    SERVE_DOCS = ['private']

    USE_PROMOS = False
    DO_NOT_TRACK_ENABLED = True


ContainerSettings.load_settings(__name__)
