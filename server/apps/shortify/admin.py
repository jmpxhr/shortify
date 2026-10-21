from typing import Final

from django.conf import settings
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import SafeString

from server.apps.shortify.infrastructure.models import ShortLink

ORIGINAL_URL_MAX_DISPLAY_LENGTH: Final = 65
FALLBACK_DOMAIN: Final = 'http://127.0.0.1:8000'


def _build_short_url(short_code: str) -> str:
    """Absolute short URL for `short_code`, based on settings.DOMAIN."""
    domain = getattr(settings, 'DOMAIN', FALLBACK_DOMAIN).rstrip('/')
    path = reverse('api:v1:redirect_link', kwargs={'short_code': short_code})
    return f'{domain}{path}'


def _render_link(url: str, label: str | None = None) -> SafeString:
    return format_html(
        '<a href="{url}" target="_blank" rel="noopener noreferrer">{label}</a>',
        url=url,
        label=label or url,
    )


@admin.register(ShortLink)
class ShortLinkAdmin(admin.ModelAdmin[ShortLink]):
    list_display = (
        'id',
        'short_code_link',
        'original_url_truncated',
        'clicks',
        'owner',
        'created_at',
    )
    list_filter = ('created_at', 'owner')
    search_fields = ('short_code', 'original_url', 'owner__username')
    list_select_related = ('owner',)
    readonly_fields = ('created_at', 'clicks', 'full_short_url')

    fieldsets = (
        (
            'General information',
            {
                'fields': [
                    'short_code',
                    'original_url',
                    'clicks',
                    'owner',
                ],
            },
        ),
        (
            'Links',
            {
                'fields': [
                    'full_short_url',
                ],
            },
        ),
        (
            'Stats and tech data',
            {
                'fields': ['created_at'],
                'classes': ['collapse'],
            },
        ),
    )

    @admin.display(description='Short code', ordering='short_code')
    def short_code_link(self, obj: ShortLink) -> SafeString:
        """Short code rendered as a clickable link."""
        url = _build_short_url(short_code=obj.short_code)
        return _render_link(url, label=obj.short_code)

    @admin.display(description='Original URL', ordering='original_url')
    def original_url_truncated(self, obj: ShortLink) -> str:
        """Truncated original URL for the changelist."""
        url = obj.original_url
        if len(url) > ORIGINAL_URL_MAX_DISPLAY_LENGTH:
            truncated_url = url[: ORIGINAL_URL_MAX_DISPLAY_LENGTH - 3]
            return f'{truncated_url}...'
        return url

    @admin.display(description='Full short URL')
    def full_short_url(self, obj: ShortLink) -> SafeString:
        """Full short URL as an anchor, for the change form."""
        url = _build_short_url(short_code=obj.short_code)
        return _render_link(url)
