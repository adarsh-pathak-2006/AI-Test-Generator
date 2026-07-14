#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files (needed for Django admin and any static assets)
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py migrate
