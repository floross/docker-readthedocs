try:
    from readthedocs.settings.sqlite import *
except ImportError:
    print "Fail to import readthedocs.settings.sqlite"

import os
environ = os.environ

SITE_ROOT = '/app'

if os.getenv('RTD_HAS_DATABASE', 'false').lower() == 'true':
    DATABASES = {
        'default': {
            'ENGINE': os.getenv('DB_ENV_ENGINE', 'django.db.backends.postgresql_psycopg2'),
            'NAME': os.getenv('DB_ENV_DB_NAME', 'reathedocs'),
            'USER': os.getenv('DB_ENV_DB_USER', 'root'),
            'PASSWORD': os.getenv('DB_ENV_DB_PASS', None),
            'HOST': os.getenv('DB_ENV_HOST', 'localhost'),
            'PORT': os.getenv('DB_ENV_PORT', 5432),
        }
    }

if os.getenv('RTD_HAS_ELASTICSEARCH', 'false').lower() == 'true':
    ES_HOSTS = [
        '{0}:{1}'.format(
            os.getenv('ELASTICSEARCH_ENV_HOST', 'localhost'),
            os.getenv('ELASTICSEARCH_ENV_PORT', '9200')
        )
    ]

if os.getenv('RTD_HAS_REDIS', 'false').lower() == 'true':
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

# Users
ADMIN_USERNAME = os.getenv('RTD_ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.getenv('RTD_ADMIN_PASSWORD', 'admin')
ADMIN_EMAIL    = os.getenv('RTD_ADMIN_EMAIL', '{0}@localhost'.format(ADMIN_USERNAME))

SLUMBER_USERNAME = os.getenv('RTD_SLUMBER_USERNAME', 'slumber')
SLUMBER_PASSWORD = os.getenv('RTD_SLUMBER_PASSWORD', 'slumber')
SLUMBER_EMAIL    = os.getenv('RTD_SLUMBER_EMAIL', '{0}@localhost'.format(SLUMBER_USERNAME))

