FROM ubuntu:latest
MAINTAINER Florian "floross" Rossiaud <o>
MAINTAINER Simon "svvac" Wachter <himself@swordofpain.net>

ENV DEBIAN_FRONTEND=noninteractive \
    APPDIR=/app \
    DJANGO_SETTINGS_MODULE=config \
    LANG=en_US.UTF-8 \
    LC_ALL=en_US.UTF-8 \
    VIRTUAL_ENV=/venv \
    PATH=/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
    PYTHON=/venv/bin/python \
    PIP=/venv/bin/pip \
    RTD_COMMIT=e4958838a512b095d0bc8cdf8617c30cc9e489d4
# RTD_COMMIT -> Use the commit `e495883` - 2016-01-06
# You can change to master but this will not ensure that the docker-compose works
# https://github.com/rtfd/readthedocs.org/archive/master.zip


# Set locale to UTF-8
RUN locale-gen en_US.UTF-8 && \
    update-locale LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 && \
    locale-gen fr_FR.UTF-8

# Update python
RUN apt-get -qq update && \
    apt-get -y -qq upgrade && \
    apt-get install -y -qq \
        python libxml2-dev libxslt1-dev expat libevent-dev wget python-dev \
        texlive texlive-latex-extra language-pack-en unzip git python-pip \
        zlib1g-dev lib32z1-dev libpq-dev gettext curl nginx && \
    apt-get clean

# Install test dependencies
RUN pip install -q \
    virtualenv \
    supervisor

# Setting up virtualenv
RUN virtualenv /venv

# Add user py
RUN adduser --gecos 'py' --disabled-password py

RUN mkdir -p $APPDIR
WORKDIR $APPDIR

# Setup read the doc

## Extract readthedocs
RUN wget -q --no-check-certificate -O /tmp/master.zip \
        https://github.com/rtfd/readthedocs.org/archive/$RTD_COMMIT.zip && \
    unzip /tmp/master.zip >/dev/null 2>/dev/null && \
    mv readthedocs.org-$RTD_COMMIT/* readthedocs.org-$RTD_COMMIT/.??* . && \
    rmdir readthedocs.org-$RTD_COMMIT && \
    rm /tmp/master.zip && \
    $PIP install -U \
        --allow-external bzr --allow-unverified bzr \
        -r $APPDIR/requirements.txt && \
    $PIP install psycopg2 && \
    $PIP install git+https://github.com/rtfd/readthedocs-sphinx-ext.git

COPY files /

RUN $PYTHON setup.py develop

## Copy special configuration for read the docs
RUN ln -s "$APPDIR/readthedocs/static/vendor" "$APPDIR/readthedocs/core/static/vendor" && \
    ln -s $APPDIR/manage.py $APPDIR/readthedocs/manage.py && \
    ln -s $APPDIR/readthedocs/core/static $APPDIR/media/ && \
    ln -s $APPDIR/readthedocs/builds/static/builds $APPDIR/media/static/builds && \
    ln -s /etc/nginx/sites-available/readthedocs /etc/nginx/sites-enabled/readthedocs && \
    rm /etc/nginx/sites-enabled/default && \
    mkdir -p $APPDIR/prod_artifacts/media && \
    chmod +x $APPDIR/bin/* && \
    chown -R py .

# Build RTD's locale files
RUN cd $APPDIR/readthedocs && \
    $PYTHON manage.py makemessages --all && \
    $PYTHON manage.py compilemessages


# Docker config
EXPOSE 80
VOLUME [ "/app" ]

CMD [ "supervisord", "-c", "/etc/supervisord.conf", "-n" ]
