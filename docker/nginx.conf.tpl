upstream django {
    server unix:{{ APP_DIR }}/app.sock;
}

server {
    listen 8000;

    access_log {{ LOG_DIR }}/nginx_access.log;
    error_log {{ LOG_DIR }}/nginx_error.log error;

    client_header_buffer_size 32k;
    large_client_header_buffers 4 32k;
    charset utf-8;
    client_max_body_size 75M;

    location /media  {
        alias {{ APP_DIR }}/media;
    }

    location /static {
        alias {{ APP_DIR }}/staticfiles;
    }

    # Finally, send all non-media requests to the Django server.
    location / {
        uwsgi_pass  django;
        include     {{ APP_DIR }}/docker/uwsgi_params;
    }
}