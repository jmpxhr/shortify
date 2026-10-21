import { HttpErrorResponse } from '@angular/common/http';

import { ApiError, ApiFieldError } from './models';

export type ApiErrorContext =
  'login' | 'sign-up' | 'logout' | 'list' | 'create-link' | 'detail' | 'delete-link' | 'session';

const FALLBACK = 'Something went wrong. Please try again.';
const NETWORK_ERROR = 'Cannot reach the server. Check your connection and try again.';

export function apiStatus(error: unknown): number | null {
  return error instanceof HttpErrorResponse ? error.status : null;
}

export function isNotFound(error: unknown): boolean {
  return apiStatus(error) === 404;
}

export function apiErrorMessage(error: unknown, context: ApiErrorContext): string {
  if (!(error instanceof HttpErrorResponse)) {
    return error instanceof Error && error.message ? error.message : FALLBACK;
  }

  if (error.status === 0) {
    return NETWORK_ERROR;
  }

  const messages = extractMessages(error.error);

  if (error.status === 401) {
    if (context === 'login') {
      return 'Invalid username or password.';
    }
    return 'Your session has expired. Please sign in again.';
  }

  if (error.status === 403) {
    return 'Your session could not be verified. Please sign in again.';
  }

  if (context === 'sign-up' && error.status === 409) {
    return 'That username is already taken.';
  }

  if (context === 'create-link' && error.status === 409) {
    return 'Could not generate a unique short code. Please try again.';
  }

  if ((context === 'create-link' || context === 'delete-link') && error.status === 404) {
    return 'That link no longer exists.';
  }

  if (context === 'detail' && error.status === 404) {
    return 'Link not found.';
  }

  if (messages.length > 0) {
    return messages.join(' ');
  }

  if (error.status >= 500) {
    return 'The server could not complete the request. Please try again.';
  }

  return FALLBACK;
}

function extractMessages(body: unknown): string[] {
  if (typeof body === 'string') {
    return body.trim() ? [body] : [];
  }

  if (!isApiError(body)) {
    return [];
  }

  if (typeof body.detail === 'string') {
    return body.detail.trim() ? [body.detail] : [];
  }

  return body.detail
    .map((item: ApiFieldError) => item.msg)
    .filter((message): message is string => Boolean(message));
}

function isApiError(value: unknown): value is ApiError {
  if (typeof value !== 'object' || value === null || !('detail' in value)) {
    return false;
  }

  const detail = (value as { detail: unknown }).detail;
  return typeof detail === 'string' || Array.isArray(detail);
}
