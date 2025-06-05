#!/usr/bin/env bash
set -eo pipefail

# Explicitly install dependencies as a test
pip install -r requirements.txt

# Navigate into your Django project directory
cd social_media_api/

# Collect static files
python manage.py collectstatic --noinput

# Run database migrations
python manage.py migrate

# Go back to the root directory
cd ..