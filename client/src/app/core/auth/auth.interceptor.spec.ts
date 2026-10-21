import { HttpClient, provideHttpClient, withInterceptors } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';

import { credentialsInterceptor } from './auth.interceptor';

describe('credentialsInterceptor', () => {
  let httpClient: HttpClient;
  let http: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        provideHttpClient(withInterceptors([credentialsInterceptor])),
        provideHttpClientTesting(),
      ],
    });
    httpClient = TestBed.inject(HttpClient);
    http = TestBed.inject(HttpTestingController);
    clearCsrfCookie();
  });

  afterEach(() => {
    http.verify();
    clearCsrfCookie();
  });

  it('sends credentials and leaves safe methods without a CSRF header', () => {
    document.cookie = 'csrftoken=token-1; path=/';

    httpClient.get('/api/v1/links/').subscribe();

    const request = http.expectOne('/api/v1/links/');
    expect(request.request.withCredentials).toBe(true);
    expect(request.request.headers.has('X-CSRFToken')).toBe(false);
    request.flush({});
  });

  it('adds the current CSRF cookie to unsafe methods', () => {
    document.cookie = 'csrftoken=token-1; path=/';

    httpClient.post('/api/v1/links/', {}).subscribe();

    const request = http.expectOne('/api/v1/links/');
    expect(request.request.withCredentials).toBe(true);
    expect(request.request.headers.get('X-CSRFToken')).toBe('token-1');
    request.flush({});
  });

  it('re-reads the cookie for every request', () => {
    document.cookie = 'csrftoken=before-login; path=/';
    httpClient.post('/api/v1/auth/', {}).subscribe();
    http.expectOne('/api/v1/auth/').flush(null);

    document.cookie = 'csrftoken=after-login; path=/';
    httpClient.post('/api/v1/links/', {}).subscribe();

    const request = http.expectOne('/api/v1/links/');
    expect(request.request.headers.get('X-CSRFToken')).toBe('after-login');
    request.flush({});
  });

  it('lets the server reject unsafe requests when the cookie is missing', () => {
    httpClient.delete('/api/v1/links/abc123/').subscribe();

    const request = http.expectOne('/api/v1/links/abc123/');
    expect(request.request.headers.has('X-CSRFToken')).toBe(false);
    request.flush(null);
  });
});

function clearCsrfCookie(): void {
  document.cookie = 'csrftoken=; Max-Age=0; path=/';
}
