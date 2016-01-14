# ReadTheDocs in Docker

A [Docker](https://hub.docker.com/r/floross/docker-readthedocs/) container for
[ReadTheDocs](https://github.com/rtfd/readthedocs.org) (RTD) which works and 
with many goodies.


## Features

  * Optional database backend
  * Optional Redis+Celery support
  * Optional ElasticSearch support (untested)
  * Painless subdomain serving (i.e. `{project}.docs.domain.com`)
  * Correctly handles alternative domain names for projects
  * Want more? Open an issue or submit a pull request!

## Installation

### Standalone

Simply launch a `docker run` with relevant params.

    $ docker run \
        -e RTD_PRODUCTION_DOMAIN=example.com \
        -e RTD_USE_SUBDOMAIN=true \
        -e RTD_ALLOW_PRIVATE_REPOS=true \
        -p 8000:80 \
        -d \
        floross/docker-readthedocs

### Compose

Create a compose file:

    $ cp docker-compose.yml{.example,}

Adjust to your desired configuration, then start:

    $ docker-compose up

## Configurations / Environments

You can configure RTD's comportment with a bunch of environment variables
described below.

### Read the docs environment

All the RTD environment are prefixed with `RTD_`

| Name                              | Description | Default value | RTD `config.py` target (if any) |
| --------------------------------- | ----------- | ------------- | ------------------------------- |
| `RTD_DEBUG`                       | Start RTD in debug mode | `'false'` | `DEBUG` |
| `RTD_ALLOW_PRIVATE_REPOS`         | Configure RTD to let you use private repository (with credential inside the url) | `'false'` | `ALLOW_PRIVATE_REPOS` |
| `RTD_ACCOUNT_EMAIL_VERIFICATION`  | If none turn off email verification | `'none'` | `ACCOUNT_EMAIL_VERIFICATION` |
| `RTD_PRODUCTION_DOMAIN`           | The production domain use for nginx and RTD to configure the urls | `'localhost:8000'` | `PRODUCTION_DOMAIN` |
| `RTD_PUBLIC_DOMAIN`               | The public domain of the application | Value of `RTD_PRODUCTION_DOMAIN` | `PUBLIC DOMAIN` |
| `RTD_USE_SUBDOMAIN`               | Disable the `/docs/<project>` RTD routes and use only the subdomain | `'false'` | `USE_SUBDOMAIN` |
| `RTD_GLOBAL_ANALYTICS_CODE`       | Your analytics code | `''` | `GLOBAL_ANALYTICS_CODE` |
| | | | |
| `RTD_ADMIN_USERNAME`              | The username of the superuser account to create | `'admin'` | - |
| `RTD_ADMIN_PASSWORD`              | The password of the superuser account to create | `'admin'` | - |
| `RTD_ADMIN_EMAIL`                 | The email address of the superuser account to create | `'{RTD_ADMIN_USERNAME}@localhost` | - |
| `RTD_SLUMBER_USERNAME`              | The username of the Slumber API account to create | `'slumber'` | `SLUMBER_USERNAME` |
| `RTD_SLUMBER_PASSWORD`              | The password of the Slumber API account to create | `'slumber'` | `SLUMBER_PASSWORD` |
| `RTD_SLUMBER_EMAIL`                 | The email address of the Slumber API account to create | `'{RTD_SLUMBER_USERNAME}@localhost` | - |
| `RTD_SLUMBER_API_HOST`            | Configure the host of the RTD slumber api | `'http://localhost:8000'` | `SLUMBER_API_HOST` |
| | | | |
| `RTD_HAS_DATABASE`                | Configure Django with a database if `'true'` (see below) | `'false'` | - |
| `RTD_HAS_ELASTICSEARCH`           | Configure the app with an ElasticSearch endpoint if `'true'` (see below) | `'false'` | - |
| `RTD_HAS_REDIS`                   | Configure the app with a Redis endpoint if `'true'` (see below) | `'false'` | - |

To enable a postgre database, an elasticsearch server or a redis you will need to configure this following environment variable to `true`: `RTD_HAS_DATABASE`, `RTD_HAS_ELASTICSEARCH`, `RTD_HAS_REDIS`

### Database (if `$RTD_HAS_DATABASE == 'true'`)

> These vars are automatically assigned by `docker-compose` from the env vars of
> the `db` container (i.e. `db`'s `DB_NAME` env var is accessible by
> `readthedocs` as `DB_ENV_DB_NAME`). If you're not using `docker-compose`, feel
> free to set these directly for the `readthedocs` container if you wish to
> connect to a database.

| Name              | Description      | Default value                             | RTD `config.py` target (if any)     |
| ----------------- | ---------------- | ----------------------------------------- | ----------------------------------- |
| `DB_ENV_ENGINE`   | Django DB engine | `'django.db.backends.postgresql_psycopg2'`| `DATABASES['default']['ENGINE']`    |
| `DB_ENV_DB_NAME`  | DB name          | `'readthedocs'`                           | `DATABASES['default']['NAME']`      |
| `DB_ENV_DB_USER`  | DB user          | `'root'`                                  | `DATABASES['default']['USER']`      |
| `DB_ENV_DB_PASS`  | DB password      | `None`                                    | `DATABASES['default']['PASSWORD']`  |
| `DB_ENV_HOST`     | DB host          | `'localhost'`                             | `DATABASES['default']['HOST']`      |
| `DB_ENV_PORT`     | DB port          | `5432`                                    | `DATABASES['default']['PORT']`      |

**These settings are *ignored* if the env var `RTD_HAS_DATABASE` is not set to
`'true'`.**

### ElasticSearch (UNTESTED) (if `$RTD_HAS_ELASTICSEARCH == 'true'`)

> These vars are automatically assigned by `docker-compose` from the env vars of
> the `elasticsearch` container (i.e. `elasticsearch`'s `HOST` env var is
> accessible by `readthedocs` as `ELASTICSEARCH_ENV_HOST`). If you're not using
> `docker-compose`, feel free to set these directly for the `readthedocs`
> container if you wish to use elasticsearch.

| Name                     | Description        | Default value | RTD `config.py` target (if any)     |
| ------------------------ | ------------------ | ------------- | ----------------------------------- |
| `ELASTICSEARCH_ENV_HOST` | Elasticsearch host | `'localhost'` | `ES_HOSTS[0]` (as `{host}:{port}`)  |
| `ELASTICSEARCH_ENV_PORT` | Elasticsearch port | `'9200'`      | `ES_HOSTS[0]` (as `{host}:{port}`)  |

**These settings are *ignored* if the env var `RTD_HAS_ELASTICSEARCH` is not set
to `'true'`.**

### Redis (if `$RTD_HAS_REDIS == 'true'`)

> These vars are automatically assigned by `docker-compose` from the env vars of
> the `redis` container (i.e. `redis`'s `HOST` env var is accessible by
> `readthedocs` as `REDIS_ENV_HOST`). If you're not using `docker-compose`, feel
> free to set these directly for the `readthedocs` container if you wish to use
> redis.

Using Redis will start a `celery` worker on `readthedocs` to handle build tasks.

| Name                     | Description        | Default value | RTD `config.py` target (if any)     |
| ------------------------ | ------------------ | ------------- | ----------------------------------- |
| `REDIS_ENV_HOST`         | Redis host         | `'localhost'` | `REDIS['host']`                     |
| `REDIS_ENV_PORT`         | Redis port         | `'6379'`      | `REDIS['port']`                     |
| `REDIS_ENV_DB`           | Redis database     | `'0'`         | `REDIS['db']`                       |

Enabling Redis will start a `celery` worker on `readthedocs` to handle build
tasks. It will also set the following flags on `config.py`:

  * `BROKER_URL` is set to `'redis://{host}:{port}/{db}'` ;
  * `CELERY_RESULT_BACKEND` is set to `'redis://{host}:{port}/{db}'` ;
  * `CELERY_ALWAYS_EAGER` is set to `False`.

**These settings are *ignored* if the env var `RTD_HAS_REDIS` is not set to
`'true'`.**


______

*Credits to [moul/docker-readthedocs](https://github.com/moul/docker-readthedocs)*

*Credits to [vassilvk/readthedocs-docker](https://github.com/vassilvk/readthedocs-docker)*

