#!/bin/bash

# Activate the virtual env
source /venv/bin/activate

# Starting Gunicorn
/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 wsgi:app &

# Starting Nginx as the main process and NOT a daemon
nginx -g 'daemon off;'
