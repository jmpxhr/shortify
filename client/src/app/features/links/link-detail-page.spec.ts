import { HttpErrorResponse } from '@angular/common/http';
import { TestBed } from '@angular/core/testing';
import { ActivatedRoute, convertToParamMap, provideRouter } from '@angular/router';
import { of, throwError } from 'rxjs';

import { LinksService } from './links.service';
import { LinkDetailPage } from './link-detail-page';

describe('LinkDetailPage', () => {
  let detail: ReturnType<typeof vi.fn>;

  beforeEach(() => {
    detail = vi.fn();

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
});

async function settle(): Promise<void> {
  await new Promise((resolve) => setTimeout(resolve));
}
