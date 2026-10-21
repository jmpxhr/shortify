import { inject } from '@angular/core';
import { ActivatedRouteSnapshot, CanActivateFn, Router, UrlTree } from '@angular/router';

import { AuthService } from './auth.service';

export const guestGuard: CanActivateFn = async (
  route: ActivatedRouteSnapshot,
  _state,
): Promise<boolean | UrlTree> => {
  void _state;
  const auth = inject(AuthService);
  const router = inject(Router);

  await auth.ensureLoaded();

  if (!auth.isAuthenticated()) {
    return true;
  }

  return router.parseUrl(safeReturnUrl(route.queryParamMap.get('returnUrl')) ?? '/links');
};

function safeReturnUrl(candidate: string | null): string | null {
  if (!candidate || !candidate.startsWith('/') || candidate.startsWith('//')) {
    return null;
  }
  return candidate;
}
