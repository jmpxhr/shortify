import { Component, computed, input, output, signal } from '@angular/core';
import { FormField, form, maxLength, pattern, required } from '@angular/forms/signals';

import { ErrorBanner } from '../../../shared/ui/error-banner';

interface LinkFormModel {
  originalUrl: string;
}

@Component({
  imports: [FormField, ErrorBanner],
  selector: 'app-link-form',
  styleUrl: './link-form.css',
  templateUrl: './link-form.html',
})
export class LinkForm {
  readonly error = input<string | null>(null);
  readonly submitting = input(false);
  readonly createRequest = output<string>();

  readonly model = signal<LinkFormModel>({ originalUrl: '' });
  protected readonly linkForm = form(this.model, (path) => {
    required(path.originalUrl, { message: 'Enter a URL to shorten.' });
    pattern(path.originalUrl, /^https?:\/\/\S+$/i, {
      message: 'Enter a complete URL starting with http:// or https://.',
    });
    maxLength(path.originalUrl, 200, {
      message: 'URLs must be 200 characters or fewer.',
    });
  });

  protected readonly urlError = computed(() => {
    const field = this.linkForm.originalUrl();
    if (!field.touched() || !field.invalid()) {
      return '';
    }
    return field.errors()[0]?.message ?? 'Enter a valid URL.';
  });

  protected submit(event: Event): void {
    event.preventDefault();
    this.linkForm().markAsTouched();

    if (!this.linkForm().valid()) {
      return;
    }

    this.createRequest.emit(this.model().originalUrl.trim());
  }

  reset(): void {
    this.linkForm().reset({ originalUrl: '' });
  }
}
