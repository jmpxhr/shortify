from typing import TYPE_CHECKING, ClassVar, Self, override

from django.db import models

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
        verbose_name='Short URL code', max_length=SHORT_URL_MAX_LENGTH
    )

    created_at = models.DateTimeField(
        verbose_name='created date',
        auto_now_add=True,
    )
    clicks = models.PositiveIntegerField(
        verbose_name='clicks count',
        default=0,
    )

    objects: ClassVar[models.Manager[Self]]  # noqa: WPS110

    class Meta(TypedModelMeta):
        verbose_name = 'Short link'
        verbose_name_plural = 'Short links'
        ordering = ('-created_at',)
        indexes = (
            models.Index(fields=['short_code']),
            models.Index(fields=['-created_at']),
        )

    @override
    def __str__(self) -> str:
        return f'ShortLink[{self.id}, {self.short_code}]'
