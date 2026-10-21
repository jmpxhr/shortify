import { TestBed } from '@angular/core/testing';
import {
  ActivatedRouteSnapshot,
  convertToParamMap,
  provideRouter,
  Router,
  RouterStateSnapshot,
  UrlTree,
} from '@angular/router';

import { authGuard } from './auth.guard';
import { AuthService } from './auth.service';
import { guestGuard } from './guest.guard';

describe('auth guards', () => {
  let auth: {
    ensureLoaded: ReturnType<typeof vi.fn>;
    isAuthenticated: ReturnType<typeof vi.fn>;
  };
  let router: Router;

  beforeEach(() => {
    auth = {
      ensureLoaded: vi.fn().mockResolvedValue(null),
      isAuthenticated: vi.fn().mockReturnValue(false),
    };

    TestBed.configureTestingModule({
      providers: [{ provide: AuthService, useValue: auth }, provideRouter([])],
    });

    router = TestBed.inject(Router);
  });

  it('redirects anonymous users to login with the attempted URL', async () => {
    const state = { url: '/links?page=2' } as RouterStateSnapshot;

    const result = await TestBed.runInInjectionContext(() =>
      authGuard({} as ActivatedRouteSnapshot, state),
    );

    expect(result).toBeInstanceOf(UrlTree);
    expect(router.serializeUrl(result as UrlTree)).toBe('/login?returnUrl=%2Flinks%3Fpage%3D2');
  });

  it('allows authenticated users through', async () => {
    auth.isAuthenticated.mockReturnValue(true);

    const result = await TestBed.runInInjectionContext(() =>
      authGuard(
        {} as ActivatedRouteSnapshot,
        {
          url: '/links',
        } as RouterStateSnapshot,
      ),
    );

    expect(result).toBe(true);
    expect(auth.ensureLoaded).toHaveBeenCalledTimes(1);
  });

  it('allows anonymous guests to see auth pages', async () => {
    const route = {
      queryParamMap: convertToParamMap({}),
    } as ActivatedRouteSnapshot;

    const result = await TestBed.runInInjectionContext(() =>
      guestGuard(route, {} as RouterStateSnapshot),
    );

    expect(result).toBe(true);
  });

  it('sends authenticated guests back to the requested page', async () => {
    auth.isAuthenticated.mockReturnValue(true);
    const route = {
      queryParamMap: convertToParamMap({ returnUrl: '/links/abc123' }),
    } as ActivatedRouteSnapshot;

    const result = await TestBed.runInInjectionContext(() =>
      guestGuard(route, {} as RouterStateSnapshot),
    );

    expect(router.serializeUrl(result as UrlTree)).toBe('/links/abc123');
  });

  it('ignores unsafe return URLs for authenticated guests', async () => {
    auth.isAuthenticated.mockReturnValue(true);
    const route = {
      queryParamMap: convertToParamMap({ returnUrl: '//evil.example.com' }),
    } as ActivatedRouteSnapshot;

    const result = await TestBed.runInInjectionContext(() =>
      guestGuard(route, {} as RouterStateSnapshot),
    );

    expect(router.serializeUrl(result as UrlTree)).toBe('/links');
  });
});
