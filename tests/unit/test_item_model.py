import pytest

from inventory.models import Barcode, Item

pytestmark = pytest.mark.django_db


def test_get_absolute_url_with_barcode(item):
    assert item.get_absolute_url() == "/item/T0001/"


def test_get_absolute_url_with_short_barcode(area, category):
    obj = Item.objects.create(
        name="SD cards",
        business_area=area,
        category=category,
    )
    Barcode.objects.create(code="M01", item=obj)

    assert obj.get_absolute_url() == "/item/M01/"


def test_get_absolute_url_without_barcode(item_without_barcode):
    pk = item_without_barcode.pk
    assert item_without_barcode.get_absolute_url() == f"/item/id/{pk}/"
