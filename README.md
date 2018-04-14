# ReadTheDocs in Docker

A [Docker](https://hub.docker.com/r/floross/docker-readthedocs/) container for
[ReadTheDocs](https://github.com/rtfd/readthedocs.org) (RTD) which works and 
with many goodies.


## Features

  * Optional database backend
  * Optional Redis cache support
  * Optional ElasticSearch support
  * Painless subdomain serving (i.e. `{project}.docs.domain.com`)
  * Correctly handles alternative domain names for projects
  * Want more? Open an issue or submit a pull request!

## Installation

### Compose

This is a preferred method. It will build and run the whole stack seamlessly.

Create an environment file based on the default one and point compose to it:

    $ export ENV_NAME=my-org
    $ cp {example,$ENV_NAME}.env && echo "RTD_ENV_FILE=$ENV_NAME.env" > .env

Adjust to your desired configuration (in `$ENV_NAME.env` file), then start:

    $ docker-compose up

### Standalone

Simply launch a `docker run` with relevant params.

    $ docker run \
        -e RTD_PRODUCTION_DOMAIN=docs.example.com \
        -e RTD_USE_SUBDOMAIN=false \
        -e RTD_ALLOW_PRIVATE_REPOS=true \
        -p 80:80 \
        -d \
        readthedocs

## Configurations / Environments

You can configure RTD's comportment with a bunch of environment variables
described below.

### Read the docs environment

All the RTD environment are prefixed with `RTD_`

| Name                             | Description | Default value | RTD `config.py` target (if any) |
| -------------------------------- | ----------- | ------------- | ------------------------------- |
| `RTD_DEBUG`                      | Start RTD in debug mode | `'false'` | `DEBUG` |
| `RTD_ALLOW_PRIVATE_REPOS`        | Configure RTD to let you use private repository (with credential inside the url) | `'false'` | `ALLOW_PRIVATE_REPOS` |
| `RTD_ACCOUNT_EMAIL_VERIFICATION` | If none turn off email verification | `'none'` | `ACCOUNT_EMAIL_VERIFICATION` |
| `RTD_PRODUCTION_DOMAIN`          | The production domain use for nginx and RTD to configure the urls | `'localhost:8000'` | `PRODUCTION_DOMAIN` |
| `RTD_PUBLIC_DOMAIN`              | The public domain of the application | Value of `RTD_PRODUCTION_DOMAIN` | `PUBLIC DOMAIN` |
| `RTD_USE_SUBDOMAIN`              | Disable the `/docs/<project>` RTD routes and use only the subdomain | `'false'` | `USE_SUBDOMAIN` |
| `RTD_GLOBAL_ANALYTICS_CODE`      | Your analytics code | `''` | `GLOBAL_ANALYTICS_CODE` |
| | | | |
| `RTD_ADMIN_USERNAME`             | The username of the superuser account to create | `'admin'` | - |
| `RTD_ADMIN_PASSWORD`             | The password of the superuser account to create | `'admin'` | - |
| `RTD_ADMIN_EMAIL`                | The email address of the superuser account to create | `'{RTD_ADMIN_USERNAME}@{PRODUCTION_DOMAIN}` | - |
| `RTD_SLUMBER_USERNAME`           | The username of the Slumber API account to create | `'slumber'` | `SLUMBER_USERNAME` |
| `RTD_SLUMBER_PASSWORD`           | The password of the Slumber API account to create | `'slumber'` | `SLUMBER_PASSWORD` |
| `RTD_SLUMBER_EMAIL`              | The email address of the Slumber API account to create | `'{RTD_SLUMBER_USERNAME}@localhost` | - |
| `RTD_SLUMBER_API_HOST`           | Configure the host of the RTD slumber api | `'http://localhost:8000'` | `SLUMBER_API_HOST` |
| | | | |
| `RTD_HAS_DATABASE`               | Configure Django with a database if `'true'` (see below) | `'false'` | - |
| `RTD_HAS_ELASTICSEARCH`          | Configure the app with an ElasticSearch endpoint if `'true'` (see below) | `'false'` | - |
| `RTD_USE_REDIS_FOR_CACHE`        | Configure the app with a Redis endpoint if `'true'` (see below) | `'false'` | - |

To enable a postgre database, an elasticsearch server or a redis (as a cache) you will need to configure this following environment variable to `true`: `RTD_HAS_DATABASE`, `RTD_HAS_ELASTICSEARCH`, `RTD_USE_REDIS_FOR_CACHE`.

## RTD components topology

When using `docker-compose`, defaults for these settings are used -
they match across component configurations.
You can change *some* of these setting via environment file.

If you're not using `docker-compose`, feel free to set these directly for the
`readthedocs` container if you wish to connect to some backend.

### Database (if `$RTD_HAS_DATABASE == 'true'`)

| Name        | Description      | Default value                             | RTD `config.py` target (if any)     |
| ----------- | ---------------- | ----------------------------------------- | ----------------------------------- |
| `DB_ENGINE` | Django DB engine | `'django.db.backends.postgresql_psycopg2'`| `DATABASES['default']['ENGINE']`    |
| `DB_NAME`   | DB name          | `'readthedocs'`                           | `DATABASES['default']['NAME']`      |
| `DB_USER`   | DB user          | `'rtd'`                                   | `DATABASES['default']['USER']`      |
| `DB_PASS`   | DB password      | `'rtd'`                                   | `DATABASES['default']['PASSWORD']`  |
| `DB_HOST`   | DB host          | `'database'`                              | `DATABASES['default']['HOST']`      |
| `DB_PORT`   | DB port          | `5432`                                    | `DATABASES['default']['PORT']`      |

**These settings are *ignored* if the env var `RTD_HAS_DATABASE` is not set to
`'true'`.**

### ElasticSearch (if `$RTD_HAS_ELASTICSEARCH == 'true'`)

| Name                 | Description        | Default value     | RTD `config.py` target (if any)     |
| -------------------- | ------------------ | ----------------- | ----------------------------------- |
| `ELASTICSEARCH_HOST` | Elasticsearch host | `'elasticsearch'` | `ES_HOSTS[0]` (as `{host}:{port}`)  |
| `ELASTICSEARCH_PORT` | Elasticsearch port | `'9200'`          | `ES_HOSTS[0]` (as `{host}:{port}`)  |

**These settings are *ignored* if the env var `RTD_HAS_ELASTICSEARCH` is not set
to `'true'`.**

### Redis

Redis is used as Celery broker and is therefore mandatory.
You can enable/disable Redis usage as a cache via `RTD_USE_REDIS_FOR_CACHE` env var.

| Name                 | Description        | Default value | RTD `config.py` target (if any)     |
| -------------------- | ------------------ | ------------- | ----------------------------------- |
| `REDIS_HOST`         | Redis host         | `'redis'`     | `REDIS['host']`                     |
| `REDIS_PORT`         | Redis port         | `'6379'`      | `REDIS['port']`                     |
| `REDIS_DB`           | Redis database     | `'0'`         | `REDIS['db']`                       |


______

*Credits to [moul/docker-readthedocs](https://github.com/moul/docker-readthedocs)*

*Credits to [vassilvk/readthedocs-docker](https://github.com/vassilvk/readthedocs-docker)*

