import { Routes } from '@angular/router';

import { authGuard } from './core/auth/auth.guard';
import { guestGuard } from './core/auth/guest.guard';

export const routes: Routes = [
  {
    path: 'login',
    canActivate: [guestGuard],
    loadComponent: () => import('./features/auth/login-page').then((module) => module.LoginPage),
  },
  {
    path: 'sign-up',
    canActivate: [guestGuard],
    loadComponent: () => import('./features/auth/sign-up-page').then((module) => module.SignUpPage),
  },
  {
    path: 'links',
    canActivate: [authGuard],
    loadComponent: () => import('./features/links/links-page').then((module) => module.LinksPage),
  },
  {
    path: 'links/:shortCode',
    canActivate: [authGuard],
    loadComponent: () =>
      import('./features/links/link-detail-page').then((module) => module.LinkDetailPage),
  },
  { path: '', pathMatch: 'full', redirectTo: 'links' },
  { path: '**', redirectTo: 'links' },
];
