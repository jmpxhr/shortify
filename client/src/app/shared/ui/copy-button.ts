import { Component, DestroyRef, inject, input, signal } from '@angular/core';

@Component({
  selector: 'app-copy-button',
  template: `
    <button class="btn btn-sm" type="button" [attr.aria-label]="label()" (click)="copy()">
      {{ copied() ? 'Copied' : 'Copy' }}
    </button>
    <span class="sr-only" role="status" aria-live="polite">
      {{ copied() ? 'Copied to clipboard' : '' }}
    </span>
  `,
})
export class CopyButton {
  readonly text = input.required<string>();
  readonly label = input('Copy to clipboard');

  protected readonly copied = signal(false);

  private readonly destroyRef = inject(DestroyRef);
  private timer: ReturnType<typeof setTimeout> | null = null;

  constructor() {
    this.destroyRef.onDestroy(() => {
      if (this.timer) {
        clearTimeout(this.timer);
      }
    });
  }

  protected async copy(): Promise<void> {
    const value = this.text();

    try {
      if (navigator.clipboard?.writeText) {
        await navigator.clipboard.writeText(value);
      } else {
        fallbackCopy(value);
      }
    } catch {
      fallbackCopy(value);
    }

    this.copied.set(true);

    if (this.timer) {
      clearTimeout(this.timer);
    }
    this.timer = setTimeout(() => {
      this.copied.set(false);
      this.timer = null;
    }, 2000);
  }
}

function fallbackCopy(value: string): void {
  const textarea = document.createElement('textarea');
  textarea.value = value;
  textarea.setAttribute('readonly', '');
  textarea.style.position = 'fixed';
  textarea.style.opacity = '0';
  document.body.appendChild(textarea);
  textarea.select();

  try {
    if (typeof document.execCommand === 'function') {
      document.execCommand('copy');
    }
  } finally {
    document.body.removeChild(textarea);
  }
}
