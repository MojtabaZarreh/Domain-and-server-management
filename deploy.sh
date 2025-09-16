#!/bin/bash

set -e
service cron start
nginx
exec gunicorn core.wsgi:application --bind 0.0.0.0:8000
