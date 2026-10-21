# Shortify client

Angular 22 single-page app for the Shortify URL shortener.

## Requirements

- Bun 1.4+
- The Django API running on `http://localhost:8000`

## Development

Install dependencies and start the dev server:

```bash
bun install
bun run start
```

Open `http://localhost:4200/`. Requests to `/api` are proxied to
`http://localhost:8000` by `proxy.conf.json`.

The app uses HttpOnly cookie authentication. Cookies are sent with every API
request, and unsafe requests include the `X-CSRFToken` header. No auth tokens
are stored in `localStorage` or `sessionStorage`.

## Scripts

```bash
bun run start        # dev server with API proxy
bun run build        # production build
bun run test         # Vitest unit tests
bun run lint         # ESLint
bun run format       # Prettier write
bun run format:check # Prettier check
```

Lint, tests, and the production build must all pass:

```bash
bun run lint && bun run test --watch=false && bun run build
```

## Structure

- `src/app/core` — API URL/models, error mapping, auth service, interceptors, guards
- `src/app/features/auth` — login and sign-up pages
- `src/app/features/links` — dashboard, detail page, link form/list
- `src/app/shared/ui` — copy button, confirm dialog, error banner
- `src/styles.css` — design tokens, resets, shared controls, light/dark themes
