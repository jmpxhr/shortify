import { HttpClient, HttpContext } from '@angular/common/http';
import { Service, computed, inject, signal } from '@angular/core';
import { firstValueFrom } from 'rxjs';

import { API_BASE_URL } from '../api/api.config';
import { LoginPayload, SignUpPayload, User } from '../api/models';
import { PASSIVE_AUTH_CHECK, SKIP_AUTH_REFRESH } from './auth-context';

export type AuthStatus = 'unknown' | 'authenticated' | 'anonymous';

interface RawUser {
  readonly id: number;
  readonly username: string;
  readonly email: string;
}

@Service()
export class AuthService {
  private readonly http = inject(HttpClient);
  private readonly baseUrl = inject(API_BASE_URL);

  private restorePromise: Promise<User | null> | null = null;

  readonly user = signal<User | null>(null);
  readonly status = signal<AuthStatus>('unknown');
  readonly isAuthenticated = computed(() => this.status() === 'authenticated');

  /**
   * Restores the session once. Multiple callers share the same request.
   */
  ensureLoaded(): Promise<User | null> {
    if (this.status() !== 'unknown') {
      return Promise.resolve(this.user());
    }

    if (this.restorePromise) {
      return this.restorePromise;
    }

    this.restorePromise = firstValueFrom(
      this.http.get<RawUser>(`${this.baseUrl}/users/me/`, {
        context: new HttpContext().set(PASSIVE_AUTH_CHECK, true),
      }),
    )
      .then((raw) => {
        const currentUser = mapUser(raw);
        this.user.set(currentUser);
        this.status.set('authenticated');
        return currentUser;
      })
      .catch(() => {
        this.clear();
        return null;
      })
      .finally(() => {
        this.restorePromise = null;
      });

    return this.restorePromise;
  }

  async login(payload: LoginPayload): Promise<User> {
    await firstValueFrom(this.http.post<void>(`${this.baseUrl}/auth/`, payload));
    const currentUser = await this.fetchCurrentUser();
    this.user.set(currentUser);
    this.status.set('authenticated');
    return currentUser;
  }

  async signUp(payload: SignUpPayload): Promise<User> {
    await firstValueFrom(this.http.post<RawUser>(`${this.baseUrl}/auth/sign-up/`, payload));
    return this.login({
      username: payload.username,
      password: payload.password,
    });
  }

  refresh(): Promise<void> {
    return firstValueFrom(
      this.http.post<void>(`${this.baseUrl}/auth/refresh/`, null, {
        context: new HttpContext().set(SKIP_AUTH_REFRESH, true),
      }),
    );
  }

  async logout(): Promise<void> {
    try {
      await firstValueFrom(this.http.post<void>(`${this.baseUrl}/auth/logout/`, null));
    } finally {
      this.clear();
    }
  }

  clear(): void {
    this.user.set(null);
    this.status.set('anonymous');
  }

  private fetchCurrentUser(): Promise<User> {
    return firstValueFrom(this.http.get<RawUser>(`${this.baseUrl}/users/me/`)).then(mapUser);
  }
}

function mapUser(raw: RawUser): User {
  return {
    id: raw.id,
    username: raw.username,
    email: raw.email,
  };
}
