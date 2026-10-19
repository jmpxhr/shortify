from dmr.routing import Router, path

from server.apps.shortify.presentation.api.rest.v1.views import (
    RedirectView,
    ShortLinkView,
)

router = Router()

_redirect_router = Router(
    prefix='s/',
    urls=[
        path('<str:short_code>/', RedirectView.as_view(), name='redirect_link'),
    ],
    tags=['Redirect'],
)

_links_router = Router(
    'links/',
    urls=[
        path('', ShortLinkView.as_view(), name='create_link'),
    ],
    tags=['Links'],
)

router.include(_redirect_router)
router.include(_links_router)
