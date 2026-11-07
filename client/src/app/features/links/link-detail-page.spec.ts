import { HttpErrorResponse } from '@angular/common/http';
import { TestBed } from '@angular/core/testing';
import { ActivatedRoute, convertToParamMap, provideRouter } from '@angular/router';
import { of, throwError } from 'rxjs';

import { LinksService } from './links.service';
import { LinkDetailPage } from './link-detail-page';

const emptyAnalytics = {
  totalClicks: 0,
  rangeClicks: 0,
  range: '30d' as const,
  countries: [],
  referrers: [],
  devices: [],
  browsers: [],
  operatingSystems: [],
};

const populatedAnalytics = {
  totalClicks: 142,
  rangeClicks: 87,
  range: '30d' as const,
  countries: [{ value: 'DE', count: 40 }],
  referrers: [{ value: 'direct', count: 12 }],
  devices: [{ value: 'mobile', count: 55 }],
  browsers: [{ value: 'Safari', count: 30 }],
  operatingSystems: [{ value: 'iOS', count: 28 }],
};

describe('LinkDetailPage', () => {
  let detail: ReturnType<typeof vi.fn>;
  let analytics: ReturnType<typeof vi.fn>;

  beforeEach(() => {
    detail = vi.fn();
    analytics = vi.fn().mockReturnValue(of(emptyAnalytics));

    TestBed.configureTestingModule({
      imports: [LinkDetailPage],
      providers: [
        provideRouter([]),
        {
          provide: ActivatedRoute,
          useValue: {
            paramMap: of(convertToParamMap({ shortCode: 'abc123' })),
          },
        },
        {
          provide: LinksService,
          useValue: {
            detail,
            analytics,
            remove: vi.fn(),
            shortUrl: (code: string) => `http://localhost/api/v1/s/${code}/`,
          },
        },
      ],
    });
  });

  it('shows a link-not-found state for a 404 response', async () => {
    detail.mockReturnValue(throwError(() => new HttpErrorResponse({ status: 404 })));

    const fixture = TestBed.createComponent(LinkDetailPage);
    fixture.detectChanges();
    await settle();
    fixture.detectChanges();

    expect(fixture.nativeElement.textContent).toContain('Link not found');
    expect(fixture.nativeElement.textContent).toContain('Back to links');
  });

  it('renders details with clicks and the creation date', async () => {
    detail.mockReturnValue(
      of({
        originalUrl: 'https://example.com/a/long/path',
        shortCode: 'abc123',
        clicks: 42,
        createdAt: '2026-10-21T09:35:00Z',
      }),
    );

    const fixture = TestBed.createComponent(LinkDetailPage);
    fixture.detectChanges();
    await settle();
    fixture.detectChanges();

    const text = fixture.nativeElement.textContent as string;
    expect(text).toContain('abc123');
    expect(text).toContain('https://example.com/a/long/path');
    expect(text).toContain('42');
    expect(text).toContain('2026');
  });

  it('renders analytics alongside the link details', async () => {
    detail.mockReturnValue(
      of({
        originalUrl: 'https://example.com/a/long/path',
        shortCode: 'abc123',
        clicks: 42,
        createdAt: '2026-10-21T09:35:00Z',
      }),
    );
    analytics.mockReturnValue(of(populatedAnalytics));

    const fixture = TestBed.createComponent(LinkDetailPage);
    fixture.detectChanges();
    await settle();
    fixture.detectChanges();

    const text = fixture.nativeElement.textContent as string;
    expect(text).toContain('Total clicks');
    expect(text).toContain('142');
    expect(text).toContain('Tracked clicks');
    expect(text).toContain('87');
    expect(text).toContain('DE');
    expect(text).toContain('Direct');
  });

  it('keeps link details when analytics fails and retries', async () => {
    detail.mockReturnValue(
      of({
        originalUrl: 'https://example.com/a/long/path',
        shortCode: 'abc123',
        clicks: 42,
        createdAt: '2026-10-21T09:35:00Z',
      }),
    );
    analytics.mockReturnValue(throwError(() => new HttpErrorResponse({ status: 500 })));

    const fixture = TestBed.createComponent(LinkDetailPage);
    fixture.detectChanges();
    await settle();
    fixture.detectChanges();

    let text = fixture.nativeElement.textContent as string;
    expect(text).toContain('https://example.com/a/long/path');
    expect(text).toContain('The server could not complete the request');

    const retryButton = fixture.nativeElement.querySelector(
      'app-error-banner button',
    ) as HTMLButtonElement;
    analytics.mockReturnValue(of(populatedAnalytics));
    retryButton.click();
    await settle();
    fixture.detectChanges();

    text = fixture.nativeElement.textContent as string;
    expect(text).toContain('DE');
  });

  it('reloads analytics when the range changes', async () => {
    detail.mockReturnValue(
      of({
        originalUrl: 'https://example.com/a/long/path',
        shortCode: 'abc123',
        clicks: 42,
        createdAt: '2026-10-21T09:35:00Z',
      }),
    );

    const fixture = TestBed.createComponent(LinkDetailPage);
    fixture.detectChanges();
    await settle();
    fixture.detectChanges();

    const select = fixture.nativeElement.querySelector(
      'app-link-analytics select',
    ) as HTMLSelectElement;
    select.value = '7d';
    select.dispatchEvent(new Event('change'));
    await settle();
    fixture.detectChanges();

    expect(analytics).toHaveBeenLastCalledWith('abc123', '7d');
  });
});

async function settle(): Promise<void> {
  await new Promise((resolve) => setTimeout(resolve));
}
