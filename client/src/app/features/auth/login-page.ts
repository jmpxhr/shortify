import { Component, computed, inject, signal } from '@angular/core';
import { FormField, form, required } from '@angular/forms/signals';
import { Router, RouterLink } from '@angular/router';

import { apiErrorMessage } from '../../core/api/api-error';
import { LoginPayload } from '../../core/api/models';
import { AuthService } from '../../core/auth/auth.service';
import { ErrorBanner } from '../../shared/ui/error-banner';

@Component({
  imports: [FormField, RouterLink, ErrorBanner],
  selector: 'app-login-page',
  styleUrl: './auth.css',
  templateUrl: './login-page.html',
})
export class LoginPage {
  private readonly auth = inject(AuthService);
  private readonly router = inject(Router);

  readonly model = signal<LoginPayload>({ username: '', password: '' });
  protected readonly loginForm = form(this.model, (path) => {
    required(path.username, { message: 'Enter your username.' });
    required(path.password, { message: 'Enter your password.' });
  });

  protected readonly usernameError = computed(() => fieldError(this.loginForm.username()));
  protected readonly passwordError = computed(() => fieldError(this.loginForm.password()));

  protected readonly showPassword = signal(false);
  protected readonly submitting = signal(false);
  protected readonly errorMessage = signal<string | null>(null);

  protected async submit(event: Event): Promise<void> {
    event.preventDefault();
    this.loginForm().markAsTouched();
    this.errorMessage.set(null);

    if (!this.loginForm().valid()) {
      return;
    }

    this.submitting.set(true);
    try {
      await this.auth.login(this.model());
      await this.router.navigateByUrl(this.returnUrl());
    } catch (error) {
      this.errorMessage.set(apiErrorMessage(error, 'login'));
    } finally {
      this.submitting.set(false);
    }
  }

  protected togglePassword(): void {
    this.showPassword.update((visible) => !visible);
  }

  private returnUrl(): string {
    const current = this.router.url;
    const queryIndex = current.indexOf('?');
    if (queryIndex === -1) {
      return '/links';
    }

    const params = new URLSearchParams(current.slice(queryIndex + 1));
    const candidate = params.get('returnUrl');
    if (!candidate || !candidate.startsWith('/') || candidate.startsWith('//')) {
      return '/links';
    }
    return candidate;
  }
}

function fieldError(field: {
  touched: () => boolean;
  invalid: () => boolean;
  errors: () => readonly { message?: string }[];
}): string {
  if (!field.touched() || !field.invalid()) {
    return '';
  }
  return field.errors()[0]?.message ?? 'Enter a valid value.';
}
