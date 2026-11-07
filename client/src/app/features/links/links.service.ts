import { HttpClient } from '@angular/common/http';
import { Service, inject } from '@angular/core';
import { Observable, map } from 'rxjs';

import { API_BASE_URL } from '../../core/api/api.config';
import {
  AnalyticsBucket,
  AnalyticsRange,
  LinkAnalytics,
  PaginatedShortLinks,
  ShortLink,
  ShortLinkDetail,
  ShortLinkPage,
} from '../../core/api/models';

interface RawShortLink {
  readonly original_url: string;
  readonly short_code: string;
  readonly clicks: number;
}

interface RawShortLinkDetail extends RawShortLink {
  readonly created_at: string;
}

interface RawShortLinkPage {
  readonly number: number;
  readonly object_list: readonly RawShortLink[];
}

interface RawAnalyticsBucket {
  readonly value: string;
  readonly count: number;
}

interface RawLinkAnalytics {
  readonly total_clicks: number;
  readonly range_clicks: number;
  readonly range: AnalyticsRange;
  readonly countries: readonly RawAnalyticsBucket[];
  readonly referrers: readonly RawAnalyticsBucket[];
  readonly devices: readonly RawAnalyticsBucket[];
  readonly browsers: readonly RawAnalyticsBucket[];
  readonly operating_systems: readonly RawAnalyticsBucket[];
}

interface RawPaginatedShortLinks {
  readonly count: number;
  readonly num_pages: number;
  readonly per_page: number;
  readonly page: RawShortLinkPage;
}

@Service()
export class LinksService {
  private readonly http = inject(HttpClient);
  private readonly baseUrl = inject(API_BASE_URL);

  list(page = 1, pageSize = 20): Observable<PaginatedShortLinks> {
    return this.http
      .get<RawPaginatedShortLinks>(`${this.baseUrl}/links/`, {
        params: { page, page_size: pageSize },
      })
      .pipe(map(mapPage));
  }

  create(originalUrl: string): Observable<ShortLink> {
    return this.http
      .post<RawShortLink>(`${this.baseUrl}/links/`, {
        original_url: originalUrl,
      })
      .pipe(map(mapShortLink));
  }

  detail(shortCode: string): Observable<ShortLinkDetail> {
    return this.http
      .get<RawShortLinkDetail>(`${this.baseUrl}/links/${encodeURIComponent(shortCode)}/`)
      .pipe(map(mapDetail));
  }

  analytics(shortCode: string, range: AnalyticsRange = '30d'): Observable<LinkAnalytics> {
    return this.http
      .get<RawLinkAnalytics>(
        `${this.baseUrl}/links/${encodeURIComponent(shortCode)}/analytics/`,
        { params: { range } },
      )
      .pipe(map(mapAnalytics));
  }

  remove(shortCode: string): Observable<void> {
    return this.http.delete<void>(`${this.baseUrl}/links/${encodeURIComponent(shortCode)}/`);
  }

  shortUrl(shortCode: string): string {
    const path = `${this.baseUrl}/s/${encodeURIComponent(shortCode)}/`;
    const origin = typeof document === 'undefined' ? 'http://localhost' : document.baseURI;
    return new URL(path, origin).toString();
  }
}

function mapShortLink(raw: RawShortLink): ShortLink {
  return {
    originalUrl: raw.original_url,
    shortCode: raw.short_code,
    clicks: raw.clicks,
  };
}

function mapDetail(raw: RawShortLinkDetail): ShortLinkDetail {
  return {
    ...mapShortLink(raw),
    createdAt: raw.created_at,
  };
}

function mapBucket(raw: RawAnalyticsBucket): AnalyticsBucket {
  return {
    value: raw.value,
    count: raw.count,
  };
}

function mapAnalytics(raw: RawLinkAnalytics): LinkAnalytics {
  return {
    totalClicks: raw.total_clicks,
    rangeClicks: raw.range_clicks,
    range: raw.range,
    countries: raw.countries.map(mapBucket),
    referrers: raw.referrers.map(mapBucket),
    devices: raw.devices.map(mapBucket),
    browsers: raw.browsers.map(mapBucket),
    operatingSystems: raw.operating_systems.map(mapBucket),
  };
}

function mapPage(raw: RawPaginatedShortLinks): PaginatedShortLinks {
  const page: ShortLinkPage = {
    number: raw.page.number,
    objectList: raw.page.object_list.map(mapShortLink),
  };

  return {
    count: raw.count,
    numPages: raw.num_pages,
    perPage: raw.per_page,
    page,
  };
}
