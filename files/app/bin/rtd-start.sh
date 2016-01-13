#!/bin/bash -x

curl -XPUT 'http://elasticsearch:9200/readthedocs/'

cd /app/readthedocs
ln -s ../manage.py .

PYTHON=/venv/bin/python
$PYTHON manage.py syncdb --noinput
$PYTHON manage.py migrate
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@localhost', 'admin')" | $PYTHON manage.py shell
$PYTHON manage.py loaddata test_data
$PYTHON manage.py makemessages --all
$PYTHON manage.py compilemessages
export C_FORCE_ROOT="true"

if [ $RTD_HAS_REDIS -eq "true" ]
then
    /venv/bin/python manage.py celeryd -Q celery,web -l INFO &
fi

/venv/bin/python manage.py runserver 0.0.0.0:8000
