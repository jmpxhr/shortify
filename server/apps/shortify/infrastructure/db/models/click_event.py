from typing import TYPE_CHECKING, ClassVar, Self, override

from django.db import models

from server.apps.shortify.domain.constants import (
    MAX_REFERER_LENGTH,
    MAX_USER_AGENT_LENGTH,
)
from server.apps.shortify.infrastructure.db.models.short_link import ShortLink

if TYPE_CHECKING:
    from django_stubs_ext.db.models import TypedModelMeta
else:
    TypedModelMeta = object


class ClickEvent(models.Model):
    link = models.ForeignKey(
        ShortLink,
        on_delete=models.CASCADE,
        related_name='click_events',
        verbose_name='short link',
    )
    referer = models.CharField(
        verbose_name='referer',
        max_length=MAX_REFERER_LENGTH,
        blank=True,
    )
    user_agent = models.CharField(
        verbose_name='user agent',
        max_length=MAX_USER_AGENT_LENGTH,
        blank=True,
    )
    country = models.CharField(
        verbose_name='country code',
        max_length=2,  # ISO 3166-1 alpha-2, e.g. 'DE'
        blank=True,
    )
    created_at = models.DateTimeField(
        verbose_name='created date',
        auto_now_add=True,
    )

    objects: ClassVar[models.Manager[Self]]  # noqa: WPS110

    class Meta(TypedModelMeta):
        verbose_name = 'Click event'
        verbose_name_plural = 'Click events'
        ordering = ('-created_at',)
        indexes = (models.Index(fields=['link', '-created_at']),)

    @override
    def __str__(self) -> str:
        return f'ClickEvent[{self.id}]'
