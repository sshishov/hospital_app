FROM alpine:latest

MAINTAINER sshishov.sshishov@gmail.com

RUN apk update && apk add \
#    bash \
#    git \
    python3 \
    python3-dev \
    supervisor \
    ca-certificates \
    uwsgi \
    py3-virtualenv \
    nginx \
    uwsgi-python3 \
    gettext \
    git

ENV TERM=xterm \
    # ensure local python is preferred over distribution python
    PATH=/usr/local/bin:$PATH \
    APP_USER=hospital \
    APP_GROUP=hospital \
    APP_NAME=hospital
ENV APP_USER_DIR=/home/$APP_USER
ENV LOG_DIR=/var/log/$APP_USER
ENV APP_DIR=$APP_USER_DIR/app
ENV VENV_DIR=$APP_USER_DIR/venv
ENV VENV_BIN=$VENV_DIR/bin

ARG APP_DIR=$APP_DIR

# Create user, home folder, log folder
RUN set -e; \
    addgroup -S $APP_GROUP; \
    adduser -S -D -h $APP_USER_DIR -s /bin/ash $APP_USER -G $APP_GROUP; \
    mkdir -p $LOG_DIR; \
    chown -R $APP_USER:$APP_GROUP $APP_USER_DIR; \
    chown -R $APP_USER:$APP_GROUP $LOG_DIR

# make some useful symlinks that are expected to exist
RUN cd /usr/local/bin \
    && ln -s /usr/bin/pip3 pip \
    && ln -s /usr/bin/python3 python \
    && ln -s /usr/bin/python3-config python-config;
RUN su $APP_USER -l -c "mkdir -p $VENV_DIR && virtualenv --system-site-packages $VENV_DIR -p python"

# Copy over python requirements and install
COPY requirements/*.txt /tmp/requirements/
RUN set -e; \
    su $APP_USER -l -c "$VENV_BIN/pip install -r /tmp/requirements/production.txt"

# Copy the archive and grant permissions
ADD docker/archive.tar.gz $APP_DIR
RUN chown -R $APP_USER:$APP_GROUP $APP_DIR
RUN set -e; \
    pip install envtpl; \
    su $APP_USER -c "envtpl -o $APP_DIR/docker/uwsgi.ini $APP_DIR/docker/uwsgi.ini.tpl --keep-template"; \
    su $APP_USER -c "envtpl -o $APP_DIR/docker/nginx.conf $APP_DIR/docker/nginx.conf.tpl --keep-template" && \
    ln -s $APP_DIR/docker/nginx.conf /etc/nginx/conf.d/app.conf;

RUN set -e; \
    su $APP_USER -l -c "$VENV_BIN/python $APP_DIR/manage.py collectstatic --no-input"; \
    su $APP_USER -l -c "$VENV_BIN/python $APP_DIR/manage.py compilemessages";

EXPOSE 8000

WORKDIR $APP_DIR

CMD ["supervisord", "-n", "-c", "/home/hospital/app/docker/supervisor-app.conf"]
