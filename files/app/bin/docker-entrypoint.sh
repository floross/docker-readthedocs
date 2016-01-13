#!/bin/sh

$PYTHON "$APPDIR/bin/dummy-templater.py" \
    "$APPDIR/nginx-vhost-template" \
    "PUBLIC_HOST_NAME=$RTD_PRODUCTION_DOMAIN" \
    > /etc/nginx/sites-available/readthedocs

supervisord -c /etc/supervisord.conf -n $@
