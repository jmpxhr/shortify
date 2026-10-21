import { HttpErrorResponse, HttpInterceptorFn, HttpRequest } from '@angular/common/http';
import { inject } from '@angular/core';
import { Router } from '@angular/router';
import { catchError, from, switchMap, throwError } from 'rxjs';

import { AUTH_REQUEST_RETRIED, PASSIVE_AUTH_CHECK, SKIP_AUTH_REFRESH } from './auth-context';
import { AuthService } from './auth.service';

const refreshInFlight = new WeakMap<AuthService, Promise<void>>();

/**
 * Refreshes an expired access token once and replays the failed request.
 * Concurrent 401 responses share a single refresh call.
 */
export const refreshInterceptor: HttpInterceptorFn = (request, next) => {
  const auth = inject(AuthService);
  const router = inject(Router);

  return next(request).pipe(
    catchError((error: unknown) => {
      if (
        !(error instanceof HttpErrorResponse) ||
        error.status !== 401 ||
        shouldSkipRefresh(request)
      ) {
        return throwError(() => error);
      }

      return from(refreshOnce(auth)).pipe(
        catchError((refreshError: unknown) => {
          auth.clear();
          return throwError(() => refreshError);
        }),
        switchMap(() =>
          next(
            request.clone({
              context: request.context.set(AUTH_REQUEST_RETRIED, true),
            }),
          ).pipe(
            catchError((retryError: unknown) => {
              if (retryError instanceof HttpErrorResponse && retryError.status === 401) {
                auth.clear();
                if (!request.context.get(PASSIVE_AUTH_CHECK)) {
                  redirectToLogin(router);
                }
              }
              return throwError(() => retryError);
            }),
          ),
        ),
      );
    }),
  );
};

function shouldSkipRefresh(request: HttpRequest<unknown>): boolean {
  return (
    request.context.get(SKIP_AUTH_REFRESH) ||
    request.context.get(AUTH_REQUEST_RETRIED) ||
    request.url.includes('/auth/')
  );
}

function refreshOnce(auth: AuthService): Promise<void> {
  let pending = refreshInFlight.get(auth);
  if (!pending) {
    pending = auth.refresh().finally(() => {
      refreshInFlight.delete(auth);
    });
    refreshInFlight.set(auth, pending);
  }
  return pending;
}

function redirectToLogin(router: Router): void {
  const returnUrl = router.url;
  if (returnUrl.startsWith('/login')) {
    return;
  }

  void router.navigate(['/login'], {
    queryParams: { returnUrl },
  });
}
