import pytest

from tests.unit.helpers import barcode_code_length

pytestmark = pytest.mark.django_db


def test_get_absolute_url_with_barcode(item):
    assert item.get_absolute_url() == "/item/T0001/"


def test_get_absolute_url_with_short_barcode(item_with_short_code):
    with barcode_code_length(1, 10):
        url = item_with_short_code.get_absolute_url()

    assert url == "/item/M01/"


def test_get_absolute_url_without_barcode(item_without_barcode):
    pk = item_without_barcode.pk
    assert item_without_barcode.get_absolute_url() == f"/item/id/{pk}/"
