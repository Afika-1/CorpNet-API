#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status.
set -o errexit

# Define the path to the virtual environment
VENV_DIR=".venv"

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv $VENV_DIR
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source $VENV_DIR/bin/activate

# Install Python dependencies from requirements.txt
echo "Installing dependencies..."
pip install -r requirements.txt

# Run Django migrations
echo "Running migrations..."
python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput

# Collect static files (if you have any, and if you're using Django's static files for admin etc.)
# If you are serving static files via a CDN or a separate service, you might not need this.
# Render automatically sets DJANGO_SETTINGS_MODULE when you specify the WSGI entry point
# so it knows where to find settings.
# echo "Collecting static files..."
# python3 manage.py collectstatic --noinput --clear

echo "Build process complete!"