import pytest

pytestmark = pytest.mark.django_db


def test_get_absolute_url_with_barcode(item):
    assert item.get_absolute_url() == "/item/T0001/"


def test_get_absolute_url_without_barcode(item_without_barcode):
    pk = item_without_barcode.pk
    assert item_without_barcode.get_absolute_url() == f"/item/id/{pk}/"
