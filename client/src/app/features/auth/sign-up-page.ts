import { Component, computed, inject, signal } from '@angular/core';
import {
  FormField,
  email,
  form,
  maxLength,
  minLength,
  pattern,
  required,
} from '@angular/forms/signals';
import { Router, RouterLink } from '@angular/router';

import { apiErrorMessage } from '../../core/api/api-error';
import { SignUpPayload } from '../../core/api/models';
import { AuthService } from '../../core/auth/auth.service';
import { ErrorBanner } from '../../shared/ui/error-banner';

@Component({
  imports: [FormField, RouterLink, ErrorBanner],
  selector: 'app-sign-up-page',
  styleUrl: './auth.css',
  templateUrl: './sign-up-page.html',
})
export class SignUpPage {
  private readonly auth = inject(AuthService);
  private readonly router = inject(Router);

  readonly model = signal<SignUpPayload>({
    username: '',
    email: '',
    password: '',
  });

  protected readonly signUpForm = form(this.model, (path) => {
    required(path.username, { message: 'Choose a username.' });
    minLength(path.username, 1, { message: 'Choose a username.' });
    maxLength(path.username, 150, {
      message: 'Usernames must be 150 characters or fewer.',
    });
    pattern(path.username, /^[\w.@+-]+$/, {
      message: 'Use only letters, digits, and @/./+/-/_ characters.',
    });

    required(path.email, { message: 'Enter your email address.' });
    email(path.email, { message: 'Enter a valid email address.' });
    maxLength(path.email, 254, {
      message: 'Email addresses must be 254 characters or fewer.',
    });

    required(path.password, { message: 'Choose a password.' });
    minLength(path.password, 8, {
      message: 'Passwords must be at least 8 characters.',
    });
    maxLength(path.password, 128, {
      message: 'Passwords must be 128 characters or fewer.',
    });
  });

  protected readonly usernameError = computed(() => fieldError(this.signUpForm.username()));
  protected readonly emailError = computed(() => fieldError(this.signUpForm.email()));
  protected readonly passwordError = computed(() => fieldError(this.signUpForm.password()));

  protected readonly showPassword = signal(false);
  protected readonly submitting = signal(false);
  protected readonly errorMessage = signal<string | null>(null);

  protected async submit(event: Event): Promise<void> {
    event.preventDefault();
    this.signUpForm().markAsTouched();
    this.errorMessage.set(null);

    if (!this.signUpForm().valid()) {
      return;
    }

    this.submitting.set(true);
    try {
      await this.auth.signUp(this.model());
      await this.router.navigateByUrl('/links');
    } catch (error) {
      this.errorMessage.set(apiErrorMessage(error, 'sign-up'));
    } finally {
      this.submitting.set(false);
    }
  }

  protected togglePassword(): void {
    this.showPassword.update((visible) => !visible);
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
