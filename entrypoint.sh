#!/bin/sh
echo "=== ENTRYPOINT STARTED ==="
python manage.py collectstatic --noinput
echo "=== COLLECTSTATIC FINISHED ==="
exec "$@"
