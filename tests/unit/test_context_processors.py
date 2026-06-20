from django.test import RequestFactory, override_settings

from inventory.context_processors import barcode_settings


def test_default_barcode_max_length():
    request = RequestFactory().get("/")
    result = barcode_settings(request)
    assert result == {"barcode_code_max_length": 6}


@override_settings(BARCODE_CODE_LENGTH=(3, 8))
def test_custom_barcode_max_length():
    request = RequestFactory().get("/")
    result = barcode_settings(request)
    assert result == {"barcode_code_max_length": 8}
