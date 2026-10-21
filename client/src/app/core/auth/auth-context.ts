import { HttpContextToken } from '@angular/common/http';

/** Prevents a request from triggering the silent token refresh flow. */
export const SKIP_AUTH_REFRESH = new HttpContextToken<boolean>(() => false);

/**
 * Marks background session restoration. A failed refresh during a passive check clears local
 * state without navigating; guards decide where the user should go.
 */
export const PASSIVE_AUTH_CHECK = new HttpContextToken<boolean>(() => false);

/** Marks a request that was already replayed once after a refresh. */
export const AUTH_REQUEST_RETRIED = new HttpContextToken<boolean>(() => false);
