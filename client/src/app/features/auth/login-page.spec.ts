import { HttpErrorResponse } from '@angular/common/http';
import { TestBed } from '@angular/core/testing';
import { provideRouter, Router } from '@angular/router';

import { AuthService } from '../../core/auth/auth.service';
import { LoginPage } from './login-page';

describe('LoginPage', () => {
  let login: ReturnType<typeof vi.fn>;
  let router: Router;

  beforeEach(() => {
    login = vi.fn().mockResolvedValue({
      id: 1,
      username: 'alice',
      email: 'alice@example.com',
    });

    TestBed.configureTestingModule({
      imports: [LoginPage],
      providers: [
        provideRouter([]),
        {
          provide: AuthService,
          useValue: { login },
        },
      ],
    });

    router = TestBed.inject(Router);
    vi.spyOn(router, 'navigateByUrl').mockResolvedValue(true);
  });

  it('shows validation errors and does not submit an empty form', async () => {
    const fixture = TestBed.createComponent(LoginPage);
    fixture.detectChanges();

    submitForm(fixture.nativeElement as HTMLElement);
    fixture.detectChanges();

    expect(login).not.toHaveBeenCalled();
    expect(fixture.nativeElement.textContent).toContain('Enter your username.');
    expect(fixture.nativeElement.textContent).toContain('Enter your password.');
  });

  it('submits valid credentials and returns to the links dashboard', async () => {
    const fixture = TestBed.createComponent(LoginPage);
    const component = fixture.componentInstance;
    component.model.set({ username: 'alice', password: 'secret' });
    fixture.detectChanges();

    submitForm(fixture.nativeElement as HTMLElement);
    await settle();
    fixture.detectChanges();

    expect(login).toHaveBeenCalledWith({
      username: 'alice',
      password: 'secret',
    });
    expect(router.navigateByUrl).toHaveBeenCalledWith('/links');
  });

  it('shows a friendly message when credentials are rejected', async () => {
    login.mockRejectedValue(
      new HttpErrorResponse({
        status: 401,
        error: { detail: [{ msg: 'No active account found.' }] },
      }),
    );

    const fixture = TestBed.createComponent(LoginPage);
    const component = fixture.componentInstance;
    component.model.set({ username: 'alice', password: 'wrong' });
    fixture.detectChanges();

    submitForm(fixture.nativeElement as HTMLElement);
    await settle();
    fixture.detectChanges();

    expect(fixture.nativeElement.textContent).toContain('Invalid username or password.');
  });

  it('returns to the requested page after login', async () => {
    vi.spyOn(router, 'url', 'get').mockReturnValue('/login?returnUrl=%2Flinks%3Fpage%3D2');

    const fixture = TestBed.createComponent(LoginPage);
    const component = fixture.componentInstance;
    component.model.set({ username: 'alice', password: 'secret' });
    fixture.detectChanges();

    submitForm(fixture.nativeElement as HTMLElement);
    await settle();

    expect(router.navigateByUrl).toHaveBeenCalledWith('/links?page=2');
  });

  it('toggles password visibility', () => {
    const fixture = TestBed.createComponent(LoginPage);
    fixture.detectChanges();

    const password = (fixture.nativeElement as HTMLElement).querySelector(
      '#password',
    ) as HTMLInputElement;
    expect(password.type).toBe('password');

    const toggle = (fixture.nativeElement as HTMLElement).querySelector(
      'button[aria-label="Show password"]',
    ) as HTMLButtonElement;
    toggle.click();
    fixture.detectChanges();

    expect(password.type).toBe('text');
  });
});

function submitForm(host: HTMLElement): void {
  host.querySelector('form')?.dispatchEvent(new Event('submit'));
}

async function settle(): Promise<void> {
  await new Promise((resolve) => setTimeout(resolve));
}
