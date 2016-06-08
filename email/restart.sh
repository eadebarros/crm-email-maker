#!/usr/bin/env bash
source /var/lib/jenkins/gitLab_source/etl/bin/activate
cd /var/lib/jenkins/gitLab_source/mkt-crm-apps
kill -r pid
uwsgi --http :8888 --wsgi-file crm/wsgi.py &
echo $!
echo $! > pid