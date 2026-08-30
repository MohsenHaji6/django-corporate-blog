#!/bin/sh
echo "=== ENTRYPOINT STARTED ==="

python manage.py migrate --noinput

echo "=== MIGRATE FINISHED ==="

python manage.py collectstatic --noinput

echo "=== COLLECTSTATIC FINISHED ==="
exec "$@"
