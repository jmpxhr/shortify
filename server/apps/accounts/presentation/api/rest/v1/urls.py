from dmr.routing import Router, path

from server.apps.accounts.presentation.api.rest.v1.views import (
    CurrentUserView,
    LoginView,
    LogoutView,
    RefreshView,
    SignUpView,
    VerifyView,
)

accounts_router = Router(
    'auth/',
    urls=[
        path('sign-up/', SignUpView.as_view(), name='sign_up'),
        path('', LoginView.as_view(), name='login'),
        path('refresh/', RefreshView.as_view(), name='refresh'),
        path('verify/', VerifyView.as_view(), name='verify'),
        path('logout/', LogoutView.as_view(), name='logout'),
    ],
    tags=['Auth'],
)

users_router = Router(
    'users/',
    urls=[
        path('me/', CurrentUserView.as_view(), name='me'),
    ],
    tags=['Users'],
)
