try:
    from readthedocs.settings.sqlite import *
except ImportError:
    print "Fail to import readthedocs.settings.sqlite"

import os
environ = os.environ

SITE_ROOT = '/app'

if 'RTD_HAS_DATABASE' in environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.getenv('DB_ENV_DB_NAME', 'reathedocs'),
            'USER': os.getenv('DB_ENV_DB_USER', 'root'),
            'PASSWORD': os.getenv('DB_ENV_DB_PASS', None),
            'HOST': os.getenv('DB_ENV_HOST', 'localhost'),
            'PORT': os.getenv('DB_ENV_PORT', 5432),
        }
    }

if 'RTD_HAS_ELASTICSEARCH' in environ:
    ES_HOSTS = [
        '{0}:{1}'.format(
            os.getenv('ELASTICSEARCH_ENV_HOST', 'localhost'),
            os.getenv('ELASTICSEARCH_ENV_PORT', '9200')
        )
    ]

if 'RTD_HAS_REDIS' in environ:
    redis_host = os.getenv('REDIS_ENV_HOST', 'localhost')
    redis_port = os.getenv('REDIS_ENV_PORT', '6379')
    redis_db   = os.getenv('REDIS_ENV_DB', '0')

    REDIS = {
        'host': redis_host,
        'port': redis_port,
        'db': redis_db,
    }

    BROKER_URL = 'redis://{0}:{1}/{2}'.format(redis_host, redis_port, redis_db)
    CELERY_RESULT_BACKEND = 'redis://{0}:{1}/{2}'.format(redis_host, redis_port, redis_db)
    CELERY_ALWAYS_EAGER = False

DEBUG = os.getenv('RTD_DEBUG', 'false').lower() == 'true'

# Enable private Git doc repositories
ALLOW_PRIVATE_REPOS = os.getenv('RTD_ALLOW_PRIVATE_REPOS', 'false').lower() == 'true'

# Turn off email verification
ACCOUNT_EMAIL_VERIFICATION = os.getenv('RTD_ACCOUNT_EMAIL_VERIFICATION', 'none')

#Environment domain

# Set this to the root domain where this RTD installation will be running
PRODUCTION_DOMAIN = os.getenv('RTD_PRODUCTION_DOMAIN', 'localhost:8000')
PUBLIC_DOMAIN = os.getenv('RTD_PUBLIC_DOMAIN', PRODUCTION_DOMAIN)
USE_SUBDOMAIN = os.getenv('RTD_USE_SUBDOMAIN', 'false').lower() == 'true'

# Set the Slumber API host
SLUMBER_API_HOST = os.getenv('RTD_SLUMBER_API_HOST', 'http://localhost:8000')

GLOBAL_ANALYTICS_CODE = os.getenv('RTD_GLOBAL_ANALYTICS_CODE', '')

FILE_SYNCER = 'privacy.backends.syncers.LocalSyncer'
