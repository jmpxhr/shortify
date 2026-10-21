# syntax = docker/dockerfile:1

# Nginx acts as a reverse proxy for gunicorn and serves static / media files
# directly from the shared docker volumes.
FROM nginx:1.29-alpine AS production_build

# Bake the config into the image, so no host mounts are required:
COPY ./docker/nginx/nginx.conf /etc/nginx/conf.d/default.conf

# Pre-create the mount points, they are shared with the `web` service:
RUN mkdir -p /var/www/django/static /var/www/django/media \
  && chown -R nginx:nginx /var/www/django

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD wget --quiet --tries=1 --spider http://localhost/healthz || exit 1
