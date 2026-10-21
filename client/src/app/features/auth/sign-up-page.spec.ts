import { TestBed } from '@angular/core/testing';
import { provideRouter, Router } from '@angular/router';

import { AuthService } from '../../core/auth/auth.service';
import { SignUpPage } from './sign-up-page';

describe('SignUpPage', () => {
  let signUp: ReturnType<typeof vi.fn>;
  let router: Router;

  beforeEach(() => {
    signUp = vi.fn().mockResolvedValue({
      id: 1,
      username: 'alice',
      email: 'alice@example.com',
    });

    TestBed.configureTestingModule({
      imports: [SignUpPage],
      providers: [
        provideRouter([]),
        {
          provide: AuthService,
          useValue: { signUp },
        },
      ],
    });

    router = TestBed.inject(Router);
    vi.spyOn(router, 'navigateByUrl').mockResolvedValue(true);
  });

  it('validates the email format before submitting', () => {
    const fixture = TestBed.createComponent(SignUpPage);
    const component = fixture.componentInstance;
    component.model.set({
      username: 'alice',
      email: 'not-an-email',
      password: 'secret123',
    });
    fixture.detectChanges();

    submitForm(fixture.nativeElement as HTMLElement);
    fixture.detectChanges();

    expect(signUp).not.toHaveBeenCalled();
    expect(fixture.nativeElement.textContent).toContain('Enter a valid email address.');
  });

  it('creates the account and navigates to the dashboard', async () => {
    const fixture = TestBed.createComponent(SignUpPage);
    const component = fixture.componentInstance;
    component.model.set({
      username: 'alice',
      email: 'alice@example.com',
      password: 'secret123',
    });
    fixture.detectChanges();

    submitForm(fixture.nativeElement as HTMLElement);
    await new Promise((resolve) => setTimeout(resolve));

    expect(signUp).toHaveBeenCalledWith({
      username: 'alice',
      email: 'alice@example.com',
      password: 'secret123',
    });
    expect(router.navigateByUrl).toHaveBeenCalledWith('/links');
  });
});

function submitForm(host: HTMLElement): void {
  host.querySelector('form')?.dispatchEvent(new Event('submit'));
}
