import { HttpErrorResponse } from '@angular/common/http';
import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { of, throwError } from 'rxjs';

import { PaginatedShortLinks, ShortLink } from '../../core/api/models';
import { LinksPage } from './links-page';
import { LinksService } from './links.service';

const aliceLink: ShortLink = {
  originalUrl: 'https://example.com/alice',
  shortCode: 'alice1',
  clicks: 2,
};

const bobLink: ShortLink = {
  originalUrl: 'https://example.com/bob',
  shortCode: 'bob222',
  clicks: 0,
};

describe('LinksPage', () => {
  let list: ReturnType<typeof vi.fn>;
  let create: ReturnType<typeof vi.fn>;
  let remove: ReturnType<typeof vi.fn>;

  beforeEach(() => {
    list = vi.fn();
    create = vi.fn();
    remove = vi.fn();

    TestBed.configureTestingModule({
      imports: [LinksPage],
      providers: [
        provideRouter([]),
        {
          provide: LinksService,
          useValue: {
            list,
            create,
            remove,
            shortUrl: (code: string) => `http://localhost/api/v1/s/${code}/`,
          },
        },
      ],
    });
  });

  it('shows an empty state when there are no links', async () => {
    list.mockReturnValue(of(page([])));

    const fixture = TestBed.createComponent(LinksPage);
    fixture.detectChanges();
    await settle();
    fixture.detectChanges();

    expect(fixture.nativeElement.textContent).toContain('No links yet');
    expect(fixture.nativeElement.textContent).toContain('0 total');
  });

  it('renders loaded links with pagination information', async () => {
    list.mockReturnValue(of(page([aliceLink, bobLink], 2, 41)));

    const fixture = TestBed.createComponent(LinksPage);
    fixture.detectChanges();
    await settle();
    fixture.detectChanges();

    const text = fixture.nativeElement.textContent as string;
    expect(text).toContain('alice1');
    expect(text).toContain('bob222');
    expect(text).toContain('Page 1 of 2');
    expect(text).toContain('41 total');
  });

  it('moves back a page after deleting the last link on it', async () => {
    list.mockImplementation((pageNumber: number) =>
      of(pageNumber === 1 ? page([aliceLink], 2, 21) : page([bobLink], 2, 21)),
    );
    remove.mockReturnValue(of(undefined));

    const fixture = TestBed.createComponent(LinksPage);
    const component = fixture.componentInstance;
    fixture.detectChanges();
    await settle();
    fixture.detectChanges();

    nextButton(fixture.nativeElement as HTMLElement).click();
    await settle();
    fixture.detectChanges();
    expect(list).toHaveBeenLastCalledWith(2, 20);

    await component.deleteLink(bobLink);

    expect(remove).toHaveBeenCalledWith('bob222');
    expect(list).toHaveBeenLastCalledWith(1, 20);
  });

  it('shows create errors from the API', async () => {
    list.mockReturnValue(of(page([])));
    create.mockReturnValue(throwError(() => new HttpErrorResponse({ status: 409 })));

    const fixture = TestBed.createComponent(LinksPage);
    const component = fixture.componentInstance;
    fixture.detectChanges();
    await settle();
    fixture.detectChanges();

    await component.createLink('https://example.com/new');
    fixture.detectChanges();

    expect(fixture.nativeElement.textContent).toContain(
      'Could not generate a unique short code. Please try again.',
    );
  });
});

function page(
  objectList: ShortLink[],
  numPages = 1,
  count = objectList.length,
): PaginatedShortLinks {
  return {
    count,
    numPages,
    perPage: 20,
    page: { number: 1, objectList },
  };
}

function nextButton(host: HTMLElement): HTMLButtonElement {
  const button = Array.from(host.querySelectorAll('button')).find(
    (candidate) => candidate.textContent?.trim() === 'Next',
  );
  if (!button) {
    throw new Error('Next button not found');
  }
  return button;
}

async function settle(): Promise<void> {
  await new Promise((resolve) => setTimeout(resolve));
}
