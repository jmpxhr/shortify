import { HttpInterceptorFn } from '@angular/common/http';

const CSRF_COOKIE = 'csrftoken';
const UNSAFE_METHODS = new Set(['POST', 'PUT', 'PATCH', 'DELETE']);

/**
 * Sends cookies with every API request and adds the CSRF token to unsafe methods.
 * The cookie is read at request time because logging in rotates it.
 */
export const credentialsInterceptor: HttpInterceptorFn = (request, next) => {
  let outgoing = request.clone({ withCredentials: true });

  if (UNSAFE_METHODS.has(request.method.toUpperCase())) {
    const token = readCookie(CSRF_COOKIE);
    if (token) {
      outgoing = outgoing.clone({
        headers: outgoing.headers.set('X-CSRFToken', token),
      });
    }
  }

  return next(outgoing);
};

export function readCookie(name: string): string | null {
  if (typeof document === 'undefined') {
    return null;
  }

  const prefix = `${name}=`;
  for (const part of document.cookie.split(';')) {
    const cookie = part.trim();
    if (cookie.startsWith(prefix)) {
      return decodeURIComponent(cookie.slice(prefix.length));
    }
  }
  return null;
}
