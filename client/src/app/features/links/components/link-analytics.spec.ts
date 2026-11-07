import { TestBed } from '@angular/core/testing';

import { AnalyticsRange, LinkAnalytics as LinkAnalyticsModel } from '../../../core/api/models';
import { LinkAnalytics } from './link-analytics';

const populated: LinkAnalyticsModel = {
  totalClicks: 142,
  rangeClicks: 87,
  range: '30d',
  countries: [{ value: 'DE', count: 40 }],
  referrers: [{ value: 'direct', count: 12 }],
  devices: [{ value: 'mobile', count: 55 }],
  browsers: [{ value: 'Safari', count: 30 }],
  operatingSystems: [{ value: 'unknown', count: 28 }],
};

describe('LinkAnalytics', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({ imports: [LinkAnalytics] });
  });

  it('renders totals and every breakdown', () => {
    const fixture = TestBed.createComponent(LinkAnalytics);
    fixture.componentRef.setInput('analytics', populated);
    fixture.detectChanges();

    const text = fixture.nativeElement.textContent as string;
    expect(text).toContain('142');
    expect(text).toContain('87');
    expect(text).toContain('Countries');
    expect(text).toContain('DE');
    expect(text).toContain('Direct');
    expect(text).toContain('mobile');
    expect(text).toContain('Safari');
    expect(text).toContain('Unknown');
  });

  it('shows an empty state while keeping the lifetime total', () => {
    const fixture = TestBed.createComponent(LinkAnalytics);
    fixture.componentRef.setInput('analytics', {
      ...populated,
      rangeClicks: 0,
      countries: [],
      referrers: [],
      devices: [],
      browsers: [],
      operatingSystems: [],
    });
    fixture.detectChanges();

    const text = fixture.nativeElement.textContent as string;
    expect(text).toContain('No tracked clicks in this range');
    expect(text).toContain('142');
  });

  it('shows a loading state', () => {
    const fixture = TestBed.createComponent(LinkAnalytics);
    fixture.componentRef.setInput('loading', true);
    fixture.detectChanges();

    expect(fixture.nativeElement.textContent).toContain('Loading analytics');
  });

  it('shows a retryable error state', () => {
    const fixture = TestBed.createComponent(LinkAnalytics);
    const retry = vi.fn();
    fixture.componentInstance.retry.subscribe(retry);
    fixture.componentRef.setInput('errorMessage', 'Analytics unavailable');
    fixture.detectChanges();

    const button = fixture.nativeElement.querySelector('button') as HTMLButtonElement;
    button.click();

    expect(fixture.nativeElement.textContent).toContain('Analytics unavailable');
    expect(retry).toHaveBeenCalledOnce();
  });

  it('emits range changes', () => {
    const fixture = TestBed.createComponent(LinkAnalytics);
    const emitted: AnalyticsRange[] = [];
    fixture.componentInstance.rangeChange.subscribe((range) => emitted.push(range));
    fixture.detectChanges();

    const select = fixture.nativeElement.querySelector('select') as HTMLSelectElement;
    select.value = '7d';
    select.dispatchEvent(new Event('change'));

    expect(emitted).toEqual(['7d']);
  });
});
