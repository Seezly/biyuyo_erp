#!/bin/sh
set -e

# Remove default nginx site that overrides our config
rm -f /etc/nginx/sites-enabled/default

# Substitute $PORT in nginx config (Render sets this env var)
envsubst '${PORT}' < /etc/nginx/conf.d/default.conf > /tmp/default.conf
mv /tmp/default.conf /etc/nginx/conf.d/default.conf

# Run migrations
cd /app/backend
python manage.py migrate --noinput

# Seed admin if DB is empty
python manage.py seed_admin

# Start supervisord (nginx + gunicorn)
exec /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf
