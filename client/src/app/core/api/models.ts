export interface User {
  readonly id: number;
  readonly username: string;
  readonly email: string;
}

export interface ShortLink {
  readonly originalUrl: string;
  readonly shortCode: string;
  readonly clicks: number;
}

export interface ShortLinkDetail extends ShortLink {
  readonly createdAt: string;
}

export interface CreateShortLinkPayload {
  readonly originalUrl: string;
}

export interface ShortLinkPage {
  readonly number: number;
  readonly objectList: ShortLink[];
}

export interface PaginatedShortLinks {
  readonly count: number;
  readonly numPages: number;
  readonly perPage: number;
  readonly page: ShortLinkPage;
}

export type AnalyticsRange = '7d' | '30d' | '90d' | 'all';

export interface AnalyticsBucket {
  readonly value: string;
  readonly count: number;
}

export interface LinkAnalytics {
  readonly totalClicks: number;
  readonly rangeClicks: number;
  readonly range: AnalyticsRange;
  readonly countries: readonly AnalyticsBucket[];
  readonly referrers: readonly AnalyticsBucket[];
  readonly devices: readonly AnalyticsBucket[];
  readonly browsers: readonly AnalyticsBucket[];
  readonly operatingSystems: readonly AnalyticsBucket[];
}

export interface ApiFieldError {
  readonly loc?: readonly (string | number)[];
  readonly msg: string;
  readonly type?: string;
}

export interface ApiError {
  readonly detail: readonly ApiFieldError[] | string;
}

export interface LoginPayload {
  readonly username: string;
  readonly password: string;
}

export interface SignUpPayload extends LoginPayload {
  readonly email: string;
}
