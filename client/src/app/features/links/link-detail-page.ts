import { Component, computed, effect, inject, signal, viewChild } from '@angular/core';
import { DatePipe } from '@angular/common';
import { toSignal } from '@angular/core/rxjs-interop';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { firstValueFrom } from 'rxjs';
import { map } from 'rxjs/operators';

import { apiErrorMessage, isNotFound } from '../../core/api/api-error';
import { ShortLinkDetail } from '../../core/api/models';
import { ConfirmDialog } from '../../shared/ui/confirm-dialog';
import { CopyButton } from '../../shared/ui/copy-button';
import { ErrorBanner } from '../../shared/ui/error-banner';
import { LinksService } from './links.service';

@Component({
  imports: [RouterLink, DatePipe, CopyButton, ConfirmDialog, ErrorBanner],
  selector: 'app-link-detail-page',
  styleUrl: './link-detail-page.css',
  templateUrl: './link-detail-page.html',
})
export class LinkDetailPage {
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  private readonly linksService = inject(LinksService);

  protected readonly shortCode = toSignal(
    this.route.paramMap.pipe(map((params) => params.get('shortCode') ?? '')),
    { initialValue: '' },
  );

  protected readonly link = signal<ShortLinkDetail | null>(null);
  protected readonly loading = signal(true);
  protected readonly notFound = signal(false);
  protected readonly errorMessage = signal<string | null>(null);
  protected readonly pendingDelete = signal(false);

  protected readonly deleteMessage = computed(() => {
    const link = this.link();
    return link ? `Delete ${link.shortCode}? The short URL will stop working.` : '';
  });

  private readonly confirmDialog = viewChild(ConfirmDialog);

  constructor() {
    effect(() => {
      const shortCode = this.shortCode();
      if (shortCode) {
        void this.load(shortCode);
      }
    });
  }

  protected async load(shortCode: string): Promise<void> {
    this.loading.set(true);
    this.errorMessage.set(null);
    this.notFound.set(false);
    this.link.set(null);

    try {
      this.link.set(await firstValueFrom(this.linksService.detail(shortCode)));
    } catch (error) {
      if (isNotFound(error)) {
        this.notFound.set(true);
      } else {
        this.errorMessage.set(apiErrorMessage(error, 'detail'));
      }
    } finally {
      this.loading.set(false);
    }
  }

  protected shortUrl(shortCode: string): string {
    return this.linksService.shortUrl(shortCode);
  }

  protected retry(): void {
    const shortCode = this.shortCode();
    if (shortCode) {
      void this.load(shortCode);
    }
  }

  protected requestDelete(): void {
    this.pendingDelete.set(true);
    this.confirmDialog()?.open();
  }

  protected onDeleteCancelled(): void {
    this.pendingDelete.set(false);
  }

  protected async confirmDelete(): Promise<void> {
    this.confirmDialog()?.close();
    this.pendingDelete.set(false);
    await this.deleteLink();
  }

  async deleteLink(): Promise<void> {
    const link = this.link();
    if (!link) {
      return;
    }

    this.errorMessage.set(null);

    try {
      await firstValueFrom(this.linksService.remove(link.shortCode));
      await this.router.navigate(['/links']);
    } catch (error) {
      if (isNotFound(error)) {
        this.notFound.set(true);
        this.link.set(null);
        return;
      }
      this.errorMessage.set(apiErrorMessage(error, 'delete-link'));
    }
  }
}
