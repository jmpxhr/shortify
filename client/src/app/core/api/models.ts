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
