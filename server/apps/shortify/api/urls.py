from dmr.routing import Router, path

from server.apps.shortify.api.views import ShortLinkView

router = Router(
    prefix='shortify/',
    urls=[path('', ShortLinkView.as_view(), name='short-link')],
    tags=['Shortify'],
)
