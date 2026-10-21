import {
  HttpClient,
  HttpContext,
  HttpErrorResponse,
  provideHttpClient,
  withInterceptors,
} from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { provideRouter, Router } from '@angular/router';

import { PASSIVE_AUTH_CHECK } from './auth-context';
import { AuthService } from './auth.service';
import { refreshInterceptor } from './refresh.interceptor';

describe('refreshInterceptor', () => {
  let httpClient: HttpClient;
  let http: HttpTestingController;
  let router: Router;
  let auth: { refresh: ReturnType<typeof vi.fn>; clear: ReturnType<typeof vi.fn> };

  beforeEach(() => {
    auth = {
      refresh: vi.fn(),
      clear: vi.fn(),
    };

    TestBed.configureTestingModule({
      providers: [
        { provide: AuthService, useValue: auth },
        provideHttpClient(withInterceptors([refreshInterceptor])),
        provideHttpClientTesting(),
        provideRouter([]),
      ],
    });

    httpClient = TestBed.inject(HttpClient);
    http = TestBed.inject(HttpTestingController);
    router = TestBed.inject(Router);
    vi.spyOn(router, 'navigate').mockResolvedValue(true);
  });

  afterEach(() => {
    http.verify();
  });

  it('refreshes once and replays the failed request', async () => {
    auth.refresh.mockResolvedValue(undefined);
    const responses: unknown[] = [];

    httpClient.get('/api/v1/links/').subscribe((value) => responses.push(value));

    http.expectOne('/api/v1/links/').flush({}, { status: 401, statusText: 'Unauthorized' });

    await settle();

    http.expectOne('/api/v1/links/').flush({ ok: true });

    expect(auth.refresh).toHaveBeenCalledTimes(1);
    expect(responses).toEqual([{ ok: true }]);
  });

  it('shares one refresh call between concurrent 401 responses', async () => {
    let resolveRefresh!: () => void;
    auth.refresh.mockReturnValue(
      new Promise<void>((resolve) => {
        resolveRefresh = resolve;
      }),
    );

    httpClient.get('/api/v1/one/').subscribe();
    httpClient.get('/api/v1/two/').subscribe();

    http.expectOne('/api/v1/one/').flush({}, { status: 401, statusText: 'Unauthorized' });
    http.expectOne('/api/v1/two/').flush({}, { status: 401, statusText: 'Unauthorized' });

    expect(auth.refresh).toHaveBeenCalledTimes(1);

    resolveRefresh();
    await settle();

    http.expectOne('/api/v1/one/').flush({ one: true });
    http.expectOne('/api/v1/two/').flush({ two: true });
  });

  it('does not refresh auth endpoints', async () => {
    const errors: unknown[] = [];

    httpClient
      .post('/api/v1/auth/verify/', {})
      .subscribe({ error: (error: unknown) => errors.push(error) });

    http.expectOne('/api/v1/auth/verify/').flush({}, { status: 401, statusText: 'Unauthorized' });

    await settle();

    expect(auth.refresh).not.toHaveBeenCalled();
    expect(errors[0]).toBeInstanceOf(HttpErrorResponse);
  });

  it('clears the session without redirecting when refresh fails', async () => {
    auth.refresh.mockRejectedValue(new Error('refresh failed'));
    const errors: unknown[] = [];

    httpClient.get('/api/v1/links/').subscribe({ error: (error: unknown) => errors.push(error) });

    http.expectOne('/api/v1/links/').flush({}, { status: 401, statusText: 'Unauthorized' });

    await settle();

    expect(auth.clear).toHaveBeenCalled();
    expect(errors).toHaveLength(1);
    expect(router.navigate).not.toHaveBeenCalled();
  });

  it('does not redirect during a passive auth check', async () => {
    auth.refresh.mockResolvedValue(undefined);
    const context = new HttpContext().set(PASSIVE_AUTH_CHECK, true);

    httpClient.get('/api/v1/users/me/', { context }).subscribe({ error: () => undefined });

    http.expectOne('/api/v1/users/me/').flush({}, { status: 401, statusText: 'Unauthorized' });

    await settle();

    http.expectOne('/api/v1/users/me/').flush({}, { status: 401, statusText: 'Unauthorized' });

    expect(auth.clear).toHaveBeenCalled();
    expect(router.navigate).not.toHaveBeenCalled();
  });

  it('redirects to login when the replayed request is rejected', async () => {
    auth.refresh.mockResolvedValue(undefined);

    httpClient.get('/api/v1/links/').subscribe({ error: () => undefined });

    http.expectOne('/api/v1/links/').flush({}, { status: 401, statusText: 'Unauthorized' });

    await settle();

    http.expectOne('/api/v1/links/').flush({}, { status: 401, statusText: 'Unauthorized' });

    expect(auth.clear).toHaveBeenCalled();
    expect(router.navigate).toHaveBeenCalledWith(['/login'], {
      queryParams: { returnUrl: '/' },
    });
  });
});

async function settle(): Promise<void> {
  await new Promise((resolve) => setTimeout(resolve));
}
