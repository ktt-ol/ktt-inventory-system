from contextlib import contextmanager
from importlib import import_module, reload

from django.conf import settings
from django.test import override_settings
from django.urls import clear_url_caches


@contextmanager
def barcode_code_length(min_len, max_len):
    """
    Apply a code length range the way a deployment configures it.

    The ``item`` pattern is compiled when the urlconf is imported, so
    overriding the setting alone leaves the old pattern in place.
    """
    with override_settings(BARCODE_CODE_LENGTH=(min_len, max_len)):
        _reload_urlconf()
        yield
    _reload_urlconf()


def _reload_urlconf():
    reload(import_module(settings.ROOT_URLCONF))
    clear_url_caches()
