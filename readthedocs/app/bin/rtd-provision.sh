#!/bin/bash -e

echo "Migrating (provisioning) the database..."
$PYTHON manage.py migrate

if [ ! -e ${APPDIR}/rtd-provisioned ]; then

    echo "Building RTD's locale files..."
    $PYTHON manage.py makemessages --all
    $PYTHON manage.py compilemessages

    echo "Generating static assets..."
    $PYTHON manage.py collectstatic --no-input

    echo "Creating users..."
    $PYTHON manage.py shell < ../bin/django-rtd-create-users.py || true

    if [ "$RTD_HAS_ELASTICSEARCH" == "true" ]; then
        echo "Provisioning Elasticsearch..."
        $PYTHON manage.py provision_elasticsearch
    fi

    touch ${APPDIR}/rtd-provisioned
fi

if [ "$RTD_HAS_ELASTICSEARCH" == "true" ]; then
    echo "Reindexing Elasticsearch..."
    $PYTHON manage.py reindex_elasticsearch
fi

echo "Starting RTD backend..."
supervisorctl start readthedocs
