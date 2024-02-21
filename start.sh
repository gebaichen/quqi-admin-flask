#! /bin/bash
cd /home/ubuntu/quqi-admin-flask
source .venv/bin/activate
exec python3 -m gunicorn --config=gunicorn.conf.py "quqi:create_app('production')"