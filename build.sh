#!/usr/bin/env bash
set -eo pipefail

# Force pip to install dependencies here
pip install -r requirements.txt

# Navigate into your Django project directory
cd social_media_api/

# Collect static files
python manage.py collectstatic --noinput

# Run database migrations
python manage.py migrate

# Go back to the root directory for the start command (THIS IS IMPORTANT FOR THE NEXT STEP'S GUNICORN COMMAND)
# cd ..