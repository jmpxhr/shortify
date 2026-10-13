from django.contrib import admin

from server.apps.shortify.models import ShortLink


@admin.register(ShortLink)
class ShortLinkAdmin(admin.ModelAdmin[ShortLink]):
    list_display = ('id', 'short_code', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('short_code', 'original_url')
