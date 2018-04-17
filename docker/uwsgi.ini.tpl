[uwsgi]
# this config will be loaded if nothing specific is specified
# load base config from below
ini = :base

# %d is the dir this configuration file is in
socket = {{ APP_DIR }}/app.sock
master = true
die-on-term = true
processes = auto
workers = 4
uid = {{ APP_GROUP }}
gid = {{ APP_USER }}
virtualenv = {{ VENV_DIR }}
plugin = python3


[dev]
ini = :base
# socket (uwsgi) is not the same as http, nor http-socket
socket = :8001


[local]
ini = :base
http = :8000
; set the virtual env to use
home = {{ VENV_DIR }}


[base]
; chdir to the folder of this config file, plus app/website
chdir = {{ APP_DIR }}
; load the module from wsgi.py, it is a python path from
; the directory above.
module = {{ APP_NAME }}.wsgi:application
; allow anyone to connect to the socket. This is very permissive
chmod-socket=666

stats = /tmp/uwsgi_stats.sock
logto = {{ LOG_DIR }}/uwsgi.log

max-requests = 100
max-requests-delta = 5

; Enable this if the app is running on a multicore machine
; cpu-affinity = 1

; prevent thundering herd
thunder-lock = true

; For newrelic
enable-threads = true
single-interpreter = true

; To support large header sizes (cookies etc)
buffer-size = 32768
post-buffering = 20971520