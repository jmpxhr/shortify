from __future__ import annotations

import secrets
import string
from typing import TYPE_CHECKING

from django.db import migrations, models

if TYPE_CHECKING:
    from django.db.backends.base.schema import BaseDatabaseSchemaEditor
    from django.db.migrations.state import StateApps

_ALPHABET = string.ascii_letters + string.digits
_CODE_LENGTH = 6
_MAX_GENERATION_ATTEMPTS = 1000


def _generate_unique_code(short_link_model: type[models.Model]) -> str:
    for _ in range(_MAX_GENERATION_ATTEMPTS):
        code = ''.join(secrets.choice(_ALPHABET) for _ in range(_CODE_LENGTH))
        if not short_link_model.objects.filter(short_code=code).exists():
            return code
    raise RuntimeError('Failed to generate a unique short code')


def dedupe_short_codes(
    apps: StateApps,
    schema_editor: BaseDatabaseSchemaEditor,
) -> None:
    """Reassign codes for duplicate rows, keeping the oldest one."""
    short_link = apps.get_model('shortify', 'ShortLink')
    duplicates = (
        short_link.objects
        .values('short_code')
        .annotate(count=models.Count('id'))
        .filter(count__gt=1)
    )
    for duplicate in duplicates:
        rows = short_link.objects.filter(
            short_code=duplicate['short_code'],
        ).order_by('id')
        for row in rows[1:]:
            row.short_code = _generate_unique_code(short_link)
            row.save(update_fields=['short_code'])


class Migration(migrations.Migration):
    dependencies = [
        ('shortify', '0002_remove_shortlink_updated_at_shortlink_clicks'),
    ]

    operations = [
        migrations.RunPython(dedupe_short_codes, migrations.RunPython.noop),
    ]
