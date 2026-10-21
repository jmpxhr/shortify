import { Component, ElementRef, input, output, viewChild } from '@angular/core';

@Component({
  selector: 'app-confirm-dialog',
  styleUrl: './confirm-dialog.css',
  template: `
    <dialog #dialog [attr.aria-label]="title()" (cancel)="onCancel($event)" (close)="onClosed()">
      <div class="confirm-dialog__body">
        <h2>{{ title() }}</h2>
        <p>{{ message() }}</p>
      </div>
      <div class="confirm-dialog__actions">
        <button #cancelButton class="btn" type="button" (click)="cancel()">Cancel</button>
        <button class="btn btn-danger" type="button" (click)="confirm()">
          {{ confirmLabel() }}
        </button>
      </div>
    </dialog>
  `,
})
export class ConfirmDialog {
  readonly title = input('Are you sure?');
  readonly message = input('This action cannot be undone.');
  readonly confirmLabel = input('Delete');

  readonly confirmed = output<void>();
  readonly cancelled = output<void>();

  private readonly dialogRef = viewChild.required<ElementRef<HTMLDialogElement>>('dialog');
  private previouslyFocused: HTMLElement | null = null;
  private resolved = false;

  open(): void {
    const dialog = this.dialogRef().nativeElement;
    if (dialog.open) {
      return;
    }

    this.resolved = false;
    this.previouslyFocused =
      document.activeElement instanceof HTMLElement ? document.activeElement : null;
    dialog.showModal();
  }

  close(): void {
    const dialog = this.dialogRef().nativeElement;
    if (!dialog.open) {
      return;
    }
    this.resolved = true;
    dialog.close();
  }

  protected confirm(): void {
    if (!this.dialogRef().nativeElement.open) {
      return;
    }
    this.resolved = true;
    this.dialogRef().nativeElement.close();
    this.confirmed.emit();
  }

  protected cancel(): void {
    if (!this.dialogRef().nativeElement.open) {
      return;
    }
    this.resolved = true;
    this.dialogRef().nativeElement.close();
    this.cancelled.emit();
  }

  protected onCancel(event: Event): void {
    event.preventDefault();
    this.cancel();
  }

  protected onClosed(): void {
    if (!this.resolved) {
      this.cancelled.emit();
    }
    this.resolved = false;

    if (this.previouslyFocused?.isConnected) {
      this.previouslyFocused.focus();
    }
    this.previouslyFocused = null;
  }
}
