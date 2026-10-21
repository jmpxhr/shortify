import { Component, input, output } from '@angular/core';

@Component({
  selector: 'app-error-banner',
  template: `
    <div class="alert" role="alert">
      <span>{{ message() }}</span>
      @if (showRetry()) {
        <button class="btn btn-sm" type="button" (click)="retry.emit()">Retry</button>
      }
    </div>
  `,
})
export class ErrorBanner {
  readonly message = input.required<string>();
  readonly showRetry = input(false);
  readonly retry = output<void>();
}
