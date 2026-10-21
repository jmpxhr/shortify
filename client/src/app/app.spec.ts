import { signal } from '@angular/core';
import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';

import { App } from './app';
import { AuthService } from './core/auth/auth.service';

describe('App', () => {
  const authenticated = signal(false);
  const user = signal<{ id: number; username: string; email: string } | null>(null);
  const logout = vi.fn().mockResolvedValue(undefined);

  beforeEach(async () => {
    authenticated.set(false);
    user.set(null);

    await TestBed.configureTestingModule({
      imports: [App],
      providers: [
        provideRouter([]),
        {
          provide: AuthService,
          useValue: {
            isAuthenticated: authenticated.asReadonly(),
            user: user.asReadonly(),
            logout,
          },
        },
      ],
    }).compileComponents();
  });

  it('renders the shell landmarks and brand', () => {
    const fixture = TestBed.createComponent(App);
    fixture.detectChanges();

    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.querySelector('.skip-link')?.textContent).toContain('Skip to content');
    expect(compiled.querySelector('.brand')?.textContent).toContain('Shortify');
    expect(compiled.querySelector('main#main-content')).toBeTruthy();
    expect(compiled.textContent).not.toContain('Log out');
  });

  it('shows the signed-in navigation and username', () => {
    authenticated.set(true);
    user.set({ id: 1, username: 'alice', email: 'alice@example.com' });

    const fixture = TestBed.createComponent(App);
    fixture.detectChanges();

    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.querySelector('.site-nav')?.textContent).toContain('Links');
    expect(compiled.textContent).toContain('alice');
    expect(compiled.textContent).toContain('Log out');
  });
});
