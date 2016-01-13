# Readthedocs in Docker

A Docker container of Readthedocs (RTD). (but this one works)

## Installation

### Standalone

To install RTD

### Compose

## Configurations / Environments

You can configure RTD's comportment with a bunch of environment variable described below.

### Read the docs environment

All the RTD environment are prefixed with `RTD_`

| Name                              | RTD `config.py` equivalent (if any) | Default                   | Description |
| ------                            | -----------               | ------------- |
| `RTD_DEBUG`                       | `DEBUG` | `'false'`                   | Start RTD in debug mode |
| `RTD_ALLOW_PRIVATE_REPOS`         | `ALLOW_PRIVATE_REPOS` | `'false'`                   | Configure RTD to let you use private repository (with credential inside the url) |
| `RTD_ACCOUNT_EMAIL_VERIFICATION`  | `ACCOUNT_EMAIL_VERIFICATION` | `'none'`                    | If none turn off email verification |
| `RTD_PRODUCTION_DOMAIN`           | `PRODUCTION_DOMAIN` | `'localhost:8000'`          | The production domain use for nginx and RTD to configure the urls |
| `RTD_PUBLIC_DOMAIN`               | `PUBLIC DOMAIN` | Value of `RTD_PRODUCTION_DOMAIN`  | The public domain of the application |
| `RTD_USE_SUBDOMAIN`               | `USE_SUBDOMAIN` | `'false'`                   | Disable the `/docs/<project>` RTD routes and use only the subdomain |
| `RTD_SLUMBER_API_HOST`            | `SLUMBER_API_HOST` | `'http://localhost:8000'`   | Configure the host of the RTD slumber api |
| `RTD_GLOBAL_ANALYTICS_CODE`       | `GLOBAL_ANALYTICS_CODE` | `''`                      | Your analytics code |

To enable a postgre database, an elasticsearch server or a redis you will need to configure this following environment variable to `true`: `RTD_HAS_DATABASE`, `RTD_HAS_ELASTICSEARCH`, `RTD_HAS_REDIS`

### Database (`if $RTD_HAS_DATABASE == 'true'`)

These vars are automatically assigned by `docker-compose` from the env vars of the `db` container (i.e. `db`'s `DB_NAME` env var is accessible by `readthedocs` as `DB_ENV_DB_NAME`). If you're not using `docker-compose`, feel free to set these directly for the `readthedocs` container.

| Name              | Default                                   | Description |
| ------            | -----------                               | ------------- |
| `DB_ENV_ENGINE`   | `'django.db.backends.postgresql_psycopg2'`| RTD db engine |
| `DB_ENV_DB_NAME`  | `'readthedocs'`                           | Db name |
| `DB_ENV_DB_USER`  | `'root'`                                  | Db user |
| `DB_ENV_DB_PASS`  | `None`                                    | Db password |
| `DB_ENV_HOST`     | `'localhost'`                             | Db host |
| `DB_ENV_PORT`     | `5432`                                    | Db port |



_____________________
*Based on moul readthedocs repository*
