"""
This is a django-split-settings main file.

To change settings file:
`DJANGO_ENV=production python manage.py runserver`
"""

from os import environ

import django_stubs_ext
from split_settings.tools import include

# Monkeypatching Django, so stubs will work for all generics,
# see: https://github.com/typeddjango/django-stubs
django_stubs_ext.monkeypatch()

# Managing environment via `DJANGO_ENV` variable:
environ.setdefault('DJANGO_ENV', 'development')
_ENV = environ['DJANGO_ENV']

_base_settings = (
    'components/common.py',
    'components/api.py',
    'components/cors.py',
    'components/caches.py',
    # Select the right env:
    f'environments/{_ENV}.py',
    # Optionally override some settings:
)

# Include settings:
include(*_base_settings)
