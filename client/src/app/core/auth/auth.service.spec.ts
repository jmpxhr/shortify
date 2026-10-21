import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';

import { PASSIVE_AUTH_CHECK } from './auth-context';
import { AuthService } from './auth.service';

const rawUser = {
  id: 1,
  username: 'alice',
  email: 'alice@example.com',
};

describe('AuthService', () => {
  let service: AuthService;
  let http: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [provideHttpClient(), provideHttpClientTesting()],
    });
    service = TestBed.inject(AuthService);
    http = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    http.verify();
  });

  it('logs in and loads the current user', async () => {
    const login = service.login({ username: 'alice', password: 'secret' });

    const loginRequest = http.expectOne('/api/v1/auth/');
    expect(loginRequest.request.method).toBe('POST');
    expect(loginRequest.request.body).toEqual({
      username: 'alice',
      password: 'secret',
    });
    loginRequest.flush(null);
    await settle();

    http.expectOne('/api/v1/users/me/').flush(rawUser);

    await expect(login).resolves.toEqual({
      id: 1,
      username: 'alice',
      email: 'alice@example.com',
    });
    expect(service.status()).toBe('authenticated');
    expect(service.isAuthenticated()).toBe(true);
  });

  it('reports login failures and keeps the user signed out', async () => {
    const login = service.login({ username: 'alice', password: 'wrong' });

    http
      .expectOne('/api/v1/auth/')
      .flush(
        { detail: [{ msg: 'No active account found.' }] },
        { status: 401, statusText: 'Unauthorized' },
      );

    await expect(login).rejects.toBeTruthy();
    expect(service.user()).toBeNull();
    expect(service.isAuthenticated()).toBe(false);
  });

  it('signs up and then logs the new account in', async () => {
    const signUp = service.signUp({
      username: 'alice',
      email: 'alice@example.com',
      password: 'secret123',
    });

    http.expectOne('/api/v1/auth/sign-up/').flush(rawUser);
    await new Promise((resolve) => setTimeout(resolve));

    http.expectOne('/api/v1/auth/').flush(null);
    await settle();
    http.expectOne('/api/v1/users/me/').flush(rawUser);

    await expect(signUp).resolves.toEqual(rawUser);
    expect(service.status()).toBe('authenticated');
  });

  it('restores the session once for concurrent callers', async () => {
    const first = service.ensureLoaded();
    const second = service.ensureLoaded();

    const request = http.expectOne('/api/v1/users/me/');
    expect(request.request.context.get(PASSIVE_AUTH_CHECK)).toBe(true);
    request.flush(rawUser);

    await expect(first).resolves.toEqual(rawUser);
    await expect(second).resolves.toEqual(rawUser);
    expect(service.isAuthenticated()).toBe(true);
  });

  it('clears state when session restoration fails', async () => {
    const restore = service.ensureLoaded();

    http
      .expectOne('/api/v1/users/me/')
      .flush({ detail: 'Not authenticated' }, { status: 401, statusText: 'Unauthorized' });

    await expect(restore).resolves.toBeNull();
    expect(service.status()).toBe('anonymous');
    expect(service.user()).toBeNull();
  });

  it('logs out and clears local state', async () => {
    const restore = service.ensureLoaded();
    http.expectOne('/api/v1/users/me/').flush(rawUser);
    await restore;

    const logout = service.logout();
    http.expectOne('/api/v1/auth/logout/').flush(null);

    await logout;
    expect(service.status()).toBe('anonymous');
    expect(service.user()).toBeNull();
  });
});

async function settle(): Promise<void> {
  await new Promise((resolve) => setTimeout(resolve));
}
