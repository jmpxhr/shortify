# django-shortify

Django URL shortener with an Angular client.

## Development

Start the backend:

```bash
docker compose up -d
```

See [`client/README.md`](client/README.md) for client details.

## GeoLite2 provisioning

Click analytics resolves country, region, and city locally with a MaxMind
GeoLite2 City database. The database is deployment data and is not committed
to the repository.

1. Create a MaxMind account and accept the GeoLite2 license:
   <https://www.maxmind.com/en/geolite2/signup>.
2. Download `GeoLite2-City.mmdb` (for example, from the MaxMind download page).
3. Place it in the host directory configured by `GEOIP_DB_HOST_DIR`
   (default: `./docker/geoip`):

   ```bash
   mkdir -p docker/geoip
   cp /path/to/GeoLite2-City.mmdb docker/geoip/GeoLite2-City.mmdb
   ```

4. Keep `GEOIP_CITY_DB_PATH` pointing at the file inside the container
   (default: `/var/lib/geoip/GeoLite2-City.mmdb`).

Both the development and production compose files mount
`GEOIP_DB_HOST_DIR` at `/var/lib/geoip` read-only. The application still
starts and redirects without a database; geolocation fields simply appear as
unknown until the file is provisioned.
