#!/usr/bin/env bash
set -eo pipefail

pip install --upgrade pip
pip install -r /home/que/Backend/requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate