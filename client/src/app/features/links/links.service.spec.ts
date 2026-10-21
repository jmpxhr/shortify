import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { firstValueFrom } from 'rxjs';

import { LinksService } from './links.service';

const rawLink = {
  original_url: 'https://example.com/path',
  short_code: 'abc123',
  clicks: 4,
};

describe('LinksService', () => {
  let service: LinksService;
  let http: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [provideHttpClient(), provideHttpClientTesting()],
    });
    service = TestBed.inject(LinksService);
    http = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    http.verify();
  });

  it('lists links with pagination and maps snake_case fields', async () => {
    const result = firstValueFrom(service.list(2, 10));

    const request = http.expectOne((candidate) => candidate.url === '/api/v1/links/');
    expect(request.request.method).toBe('GET');
    expect(request.request.params.get('page')).toBe('2');
    expect(request.request.params.get('page_size')).toBe('10');

    request.flush({
      count: 21,
      num_pages: 3,
      per_page: 10,
      page: {
        number: 2,
        object_list: [rawLink],
      },
    });

    await expect(result).resolves.toEqual({
      count: 21,
      numPages: 3,
      perPage: 10,
      page: {
        number: 2,
        objectList: [
          {
            originalUrl: 'https://example.com/path',
            shortCode: 'abc123',
            clicks: 4,
          },
        ],
      },
    });
  });

  it('creates links with the expected request body', async () => {
    const result = firstValueFrom(service.create('https://example.com/path'));

    const request = http.expectOne('/api/v1/links/');
    expect(request.request.method).toBe('POST');
    expect(request.request.body).toEqual({
      original_url: 'https://example.com/path',
    });
    request.flush(rawLink);

    await expect(result).resolves.toEqual({
      originalUrl: 'https://example.com/path',
      shortCode: 'abc123',
      clicks: 4,
    });
  });

  it('maps link details including created_at', async () => {
    const result = firstValueFrom(service.detail('abc123'));

    http
      .expectOne('/api/v1/links/abc123/')
      .flush({ ...rawLink, created_at: '2026-10-21T09:35:00Z' });

    await expect(result).resolves.toEqual({
      originalUrl: 'https://example.com/path',
      shortCode: 'abc123',
      clicks: 4,
      createdAt: '2026-10-21T09:35:00Z',
    });
  });

  it('deletes links', async () => {
    const result = firstValueFrom(service.remove('abc123'));

    const request = http.expectOne('/api/v1/links/abc123/');
    expect(request.request.method).toBe('DELETE');
    request.flush(null);

    await expect(result).resolves.toBeNull();
  });

  it('builds short URLs relative to the app origin', () => {
    expect(service.shortUrl('abc123')).toBe(
      new URL('/api/v1/s/abc123/', document.baseURI).toString(),
    );
  });
});
