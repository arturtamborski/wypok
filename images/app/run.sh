#!/bin/sh

cd /app


if [ "$1" = "manage" ]; then
  shift

  if [ "$1" = "cleanmigrations" ]; then
    find . -path '*/migrations/*.py' -not -name '__init__.py' -delete
    find . -path '*/migrations/__pycache__/*.pyc' -not -name '__init__.py' -delete
    exit $?
  fi

  python ./manage.py $@
  exit $?
fi

gunicorn -c /etc/wypok/gunicorn.conf.py wypok.wsgi
