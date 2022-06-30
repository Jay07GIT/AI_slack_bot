#!/bin/sh
exec gunicorn -b :5050 --access-logfile - --error-logfile - bot:app - --timeout=3000
