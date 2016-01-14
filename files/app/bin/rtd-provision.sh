#!/bin/bash -x

if [[ "$RTD_HAS_ELASTICSEARCH" == "true" ]]
then
    echo "Provisioning Elasticsearch..."
    curl -XPUT 'http://$ELASTICSEARCH_ENV_HOST:$ELASTICSEARCH_ENV_PORT/readthedocs/'
fi

echo "Provisionning database..."
$PYTHON manage.py syncdb --noinput
$PYTHON manage.py migrate

echo "Creating users..."
$PYTHON manage.py shell < ../bin/django-rtd-create-users.py

if [[ "$RTD_HAS_REDIS" == "true" ]]
then
    echo "Starting Celery..."
    supervisorctl start readthedocs-celery
fi
