#!/bin/sh

echo 'starting application'
gunicorn --timeout 0 -b 0.0.0.0:8080 wsgi:app