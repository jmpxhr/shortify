# django-shortify

Django URL shortener with an Angular client.

## Development

Start the backend:

```bash
just run
```

Start the Angular client in a second terminal:

```bash
just client-dev
```

The client runs at `http://localhost:4200/` and proxies `/api` requests to
`http://localhost:8000`.

Client checks:

```bash
just client-lint
just client-test
just client-build
```

See [`client/README.md`](client/README.md) for client details.
