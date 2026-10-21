import { Component, computed, inject, signal, viewChild } from '@angular/core';
import { firstValueFrom } from 'rxjs';

import { apiErrorMessage, isNotFound } from '../../core/api/api-error';
import { PaginatedShortLinks, ShortLink } from '../../core/api/models';
import { ConfirmDialog } from '../../shared/ui/confirm-dialog';
import { ErrorBanner } from '../../shared/ui/error-banner';
import { LinkForm } from './components/link-form';
import { LinkList } from './components/link-list';
import { LinksService } from './links.service';

@Component({
  imports: [LinkForm, LinkList, ConfirmDialog, ErrorBanner],
  selector: 'app-links-page',
  styleUrl: './links-page.css',
  templateUrl: './links-page.html',
})
export class LinksPage {
  private readonly linksService = inject(LinksService);

  protected readonly pageSize = 20;
  protected readonly page = signal(1);
  protected readonly data = signal<PaginatedShortLinks | null>(null);
  protected readonly loading = signal(true);
  protected readonly listError = signal<string | null>(null);
  protected readonly createError = signal<string | null>(null);
  protected readonly creating = signal(false);
  protected readonly notice = signal<string | null>(null);
  protected readonly pendingDelete = signal<ShortLink | null>(null);

  protected readonly links = computed(() => this.data()?.page.objectList ?? []);
  protected readonly totalPages = computed(() => Math.max(1, this.data()?.numPages ?? 1));
  protected readonly totalCount = computed(() => this.data()?.count ?? 0);
  protected readonly deleteMessage = computed(() => {
    const link = this.pendingDelete();
    return link ? `Delete ${link.shortCode}? The short URL will stop working.` : '';
  });

  private readonly linkForm = viewChild(LinkForm);
  private readonly confirmDialog = viewChild(ConfirmDialog);

  constructor() {
    void this.load();
  }

  protected async load(): Promise<void> {
    this.loading.set(true);
    this.listError.set(null);

    try {
      this.data.set(await firstValueFrom(this.linksService.list(this.page(), this.pageSize)));
    } catch (error) {
      this.listError.set(apiErrorMessage(error, 'list'));
    } finally {
      this.loading.set(false);
    }
  }

  protected async goToPage(page: number): Promise<void> {
    const target = Math.min(Math.max(1, page), this.totalPages());
    if (target === this.page()) {
      return;
    }
    this.page.set(target);
    await this.load();
  }

  async createLink(originalUrl: string): Promise<void> {
    this.createError.set(null);
    this.notice.set(null);
    this.creating.set(true);

    try {
      await firstValueFrom(this.linksService.create(originalUrl));
      this.linkForm()?.reset();
      this.notice.set('Short link created.');
      this.page.set(1);
      await this.load();
    } catch (error) {
      this.createError.set(apiErrorMessage(error, 'create-link'));
    } finally {
      this.creating.set(false);
    }
  }

  protected requestDelete(link: ShortLink): void {
    this.pendingDelete.set(link);
    this.confirmDialog()?.open();
  }

  protected onDeleteCancelled(): void {
    this.pendingDelete.set(null);
  }

  protected async confirmDelete(): Promise<void> {
    const link = this.pendingDelete();
    this.confirmDialog()?.close();
    this.pendingDelete.set(null);

    if (!link) {
      return;
    }

    await this.deleteLink(link);
  }

  async deleteLink(link: ShortLink): Promise<void> {
    this.listError.set(null);
    this.notice.set(null);

    try {
      await firstValueFrom(this.linksService.remove(link.shortCode));

      if (this.links().length === 1 && this.page() > 1) {
        this.page.update((current) => current - 1);
      }
      await this.load();
    } catch (error) {
      if (isNotFound(error)) {
        await this.load();
        this.notice.set('That link no longer exists.');
        return;
      }
      this.listError.set(apiErrorMessage(error, 'delete-link'));
    }
  }
}
