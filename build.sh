#!/usr/bin/env bash
set -eo pipefail

pip install --upgrade pip
pip install -r requirements.txt
cd social_media_api/
python manage.py collectstatic --noinput
python manage.py migrate