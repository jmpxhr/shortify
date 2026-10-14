from dmr.routing import Router, path

from server.apps.shortify.presentation.api.rest.views import RedirectView, ShortLinkView

router = Router(
    prefix='shortify/',
    urls=[
        path('', ShortLinkView.as_view(), name='create_link'),
        path('<str:short_code>/', RedirectView.as_view(), name='redirect_link'),
    ],
    tags=['shortify'],
)
