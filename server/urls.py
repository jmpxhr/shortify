"""
URL configuration for server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.contrib import admin
from django.contrib.admindocs import urls as admindocs_urls
from django.urls import include, path
from django.views.generic import TemplateView
from dmr.openapi import build_schema
from dmr.openapi.views import OpenAPIJsonView, SwaggerView
from dmr.plugins.msgspec import MsgspecSerializer
from dmr.routing import Router, build_404_handler, build_500_handler

from server.apps.shortify.presentation.api.rest.v1.urls import router as shortify_router

admin.autodiscover()

router = Router('api/')
v1_router = Router('v1/')
v1_router.include(shortify_router)

router.include(v1_router)

schema = build_schema(router)

handler404 = build_404_handler(router.prefix, serializer=MsgspecSerializer)
handler500 = build_500_handler(router.prefix, serializer=MsgspecSerializer)

urlpatterns = [
    # API:
    router.to_urlpatterns(namespace='api'),
    # OpenAPI:
    path(
        'docs/openapi.json/',
        OpenAPIJsonView.as_view(schema),
        name='openapi_json',
    ),
    path('docs/', SwaggerView.as_view(schema), name='swagger'),
    # django-admin:
    path('admin/doc/', include(admindocs_urls)),
    path('admin/', admin.site.urls),
    # Text and xml static files:
    path(
        'robots.txt',
        TemplateView.as_view(
            template_name='common/txt/robots.txt',
            content_type='text/plain',
        ),
        name='robots_txt',
    ),
]

if settings.DEBUG:
    import debug_toolbar
    from django.conf.urls.static import static

    urlpatterns = [
        # URLs specific only to django-debug-toolbar:
        path('__debug__/', include(debug_toolbar.urls)),
        *urlpatterns,
        # Serving media files in development only:
        *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    ]
