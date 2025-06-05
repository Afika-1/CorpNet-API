# Backend/build.sh
#/usr/bin/env bash
# Exit immediately if a command exits with a non-zero status.
set -eo pipefail

# Activate your virtual environment
# source .venv/bin/activate

# Navigate into your Django project directory
cd social_media_api/

# Collect static files (even for API, needed for Admin/DRF browsable API)
python manage.py collectstatic --noinput

# Run database migrations
python manage.py migrate

# Go back to the root directory for the start command
cd ..