import { Component, input, output } from '@angular/core';

import { AnalyticsRange, LinkAnalytics as LinkAnalyticsModel } from '../../../core/api/models';
import { ErrorBanner } from '../../../shared/ui/error-banner';

interface RangeOption {
  readonly value: AnalyticsRange;
  readonly label: string;
}

@Component({
  imports: [ErrorBanner],
  selector: 'app-link-analytics',
  styleUrl: './link-analytics.css',
  templateUrl: './link-analytics.html',
})
export class LinkAnalytics {
  readonly analytics = input<LinkAnalyticsModel | null>(null);
  readonly loading = input(false);
  readonly errorMessage = input<string | null>(null);
  readonly range = input<AnalyticsRange>('30d');
  readonly rangeChange = output<AnalyticsRange>();
  readonly retry = output<void>();

  protected readonly ranges: readonly RangeOption[] = [
    { value: '7d', label: 'Last 7 days' },
    { value: '30d', label: 'Last 30 days' },
    { value: '90d', label: 'Last 90 days' },
    { value: 'all', label: 'All time' },
  ];

  protected onRangeChange(event: Event): void {
    const select = event.target as HTMLSelectElement;
    this.rangeChange.emit(select.value as AnalyticsRange);
  }

  protected label(value: string): string {
    if (value === 'unknown') {
      return 'Unknown';
    }
    if (value === 'direct') {
      return 'Direct';
    }
    return value;
  }
}
