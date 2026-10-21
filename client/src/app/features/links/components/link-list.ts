import { Component, inject, input, output } from '@angular/core';
import { RouterLink } from '@angular/router';

import { ShortLink } from '../../../core/api/models';
import { CopyButton } from '../../../shared/ui/copy-button';
import { LinksService } from '../links.service';

@Component({
  imports: [RouterLink, CopyButton],
  selector: 'app-link-list',
  styleUrl: './link-list.css',
  templateUrl: './link-list.html',
})
export class LinkList {
  readonly links = input.required<readonly ShortLink[]>();
  readonly deleteRequest = output<ShortLink>();

  private readonly linksService = inject(LinksService);

  protected shortUrl(shortCode: string): string {
    return this.linksService.shortUrl(shortCode);
  }
}
