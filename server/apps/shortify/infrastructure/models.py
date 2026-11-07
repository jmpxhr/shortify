from typing import TYPE_CHECKING, ClassVar, Self, override

from django.conf import settings
from django.db import models

from server.apps.shortify.domain.click_constants import (
    BROWSER_MAX_LENGTH,
    CITY_MAX_LENGTH,
    COUNTRY_CODE_MAX_LENGTH,
    DEVICE_TYPE_MAX_LENGTH,
    OS_MAX_LENGTH,
    REFERRER_HOST_MAX_LENGTH,
    REGION_MAX_LENGTH,
)
from server.apps.shortify.domain.constants import (
    ORIGINAL_URL_MAX_LENGTH,
    SHORT_URL_MAX_LENGTH,
)

if TYPE_CHECKING:
    from django_stubs_ext.db.models import TypedModelMeta
else:
    TypedModelMeta = object


class ShortLink(models.Model):
    original_url = models.CharField(
        verbose_name='Original URL',
        max_length=ORIGINAL_URL_MAX_LENGTH,
    )
    short_code = models.CharField(
        verbose_name='Short URL code',
        max_length=SHORT_URL_MAX_LENGTH,
        unique=True,
    )

    created_at = models.DateTimeField(
        verbose_name='created date',
        auto_now_add=True,
    )
    clicks = models.PositiveIntegerField(
        verbose_name='clicks count',
        default=0,
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='owner',
        on_delete=models.CASCADE,
        related_name='short_links',
        null=True,
        blank=True,
    )
    owner_id: int

    objects: ClassVar[models.Manager[Self]]  # noqa: WPS110

    class Meta(TypedModelMeta):
        verbose_name = 'Short link'
        verbose_name_plural = 'Short links'
        ordering = ('-created_at',)
        indexes = (
            models.Index(fields=['-created_at']),
            models.Index(fields=['owner', '-created_at']),
        )

    @override
    def __str__(self) -> str:
        return f'ShortLink[{self.id}, {self.short_code}]'


class ClickEvent(models.Model):
    short_link = models.ForeignKey(
        ShortLink,
        verbose_name='short link',
        on_delete=models.CASCADE,
        related_name='click_events',
    )
    clicked_at = models.DateTimeField(
        verbose_name='clicked at',
        auto_now_add=True,
    )
    country_code = models.CharField(
        verbose_name='country code',
        max_length=COUNTRY_CODE_MAX_LENGTH,
        null=True,
        blank=True,
    )
    region = models.CharField(
        verbose_name='region',
        max_length=REGION_MAX_LENGTH,
        null=True,
        blank=True,
    )
    city = models.CharField(
        verbose_name='city',
        max_length=CITY_MAX_LENGTH,
        null=True,
        blank=True,
    )
    referrer_host = models.CharField(
        verbose_name='referrer host',
        max_length=REFERRER_HOST_MAX_LENGTH,
        null=True,
        blank=True,
    )
    device_type = models.CharField(
        verbose_name='device type',
        max_length=DEVICE_TYPE_MAX_LENGTH,
        null=True,
        blank=True,
    )
    browser = models.CharField(
        verbose_name='browser',
        max_length=BROWSER_MAX_LENGTH,
        null=True,
        blank=True,
    )
    os = models.CharField(
        verbose_name='operating system',
        max_length=OS_MAX_LENGTH,
        null=True,
        blank=True,
    )

    objects: ClassVar[models.Manager[Self]]  # noqa: WPS110

    class Meta(TypedModelMeta):
        verbose_name = 'Click event'
        verbose_name_plural = 'Click events'
        ordering = ('-clicked_at', '-pk')
        indexes = (models.Index(fields=['short_link', '-clicked_at']),)

    @override
    def __str__(self) -> str:
        return f'ClickEvent[{self.id}, {self.short_link_id}]'
