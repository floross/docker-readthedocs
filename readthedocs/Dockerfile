FROM debian:stretch-slim
LABEL maintainer='\
Florian "floross" Rossiaud <o>, \
Simon "svvac" Wachter <himself@swordofpain.net>, \
Yevgeny Popovych <jmennius@gmail.com>'

ENV DEBIAN_FRONTEND=noninteractive \
    APPDIR=/app \
    DJANGO_SETTINGS_MODULE=readthedocs.settings.container \
    LANG=en_US.UTF-8 \
    LC_ALL=en_US.UTF-8 \
    VIRTUAL_ENV=/venv \
    PATH=/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
    PYTHON=/venv/bin/python \
    PIP="/venv/bin/pip --disable-pip-version-check" \
    RTD_REF=2.5.0


# Set locale to UTF-8
RUN apt-get -qq update && \
    echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    apt-get install -y locales && \
    rm -rf /var/lib/apt/lists/*

# Install basic dependencies
RUN apt-get -qq update && \
    apt-get install -qq --no-install-recommends \
        python-setuptools build-essential python-dev python-pip git libevent-dev \
        libxml2-dev libxslt1-dev gettext texlive texlive-latex-extra \
        wget \
        nginx && \
    rm -rf /var/lib/apt/lists/*

# Install test dependencies
RUN pip install wheel && pip install \
    virtualenv \
    supervisor

# Setting up virtualenv
RUN virtualenv /venv

# Add user py
RUN adduser --gecos 'py' --disabled-password py

RUN mkdir -p $APPDIR
WORKDIR $APPDIR

# Setup read the docs

## Extract readthedocs
RUN wget -q --no-check-certificate -O - \
        https://github.com/rtfd/readthedocs.org/archive/${RTD_REF}.tar.gz | \
        tar -xzf - --strip-components 1 && \
    $PIP install -U -r $APPDIR/requirements/deploy.txt && \
    $PIP install elasticsearch==1.7.0 && \
    $PIP install git+https://github.com/rtfd/readthedocs-sphinx-ext.git

## Copy configuration, scripts and patch RTD
COPY . /
RUN find /patches -type f -exec patch -p1 -i {} \; && rm -rf /patches

## Copy special configuration for read the docs
RUN ln -s $APPDIR/manage.py $APPDIR/readthedocs/manage.py && \
    ln -s /etc/nginx/sites-available/readthedocs /etc/nginx/sites-enabled/readthedocs && \
    rm /etc/nginx/sites-enabled/default && \
    chmod +x $APPDIR/bin/* && \
    chown -R py .


# Docker config
EXPOSE 80
VOLUME [ "/app/user_builds" ]

CMD [ "supervisord", "-c", "/etc/supervisord.conf", "-n" ]
