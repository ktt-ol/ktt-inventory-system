import pytest

from inventory.models import BusinessArea, Category, Item

pytestmark = pytest.mark.django_db


def test_get_absolute_url_with_barcode():
    item = Item.objects.get(name="Soldering iron")
    assert item.get_absolute_url() == "/item/A0001/"


def test_get_absolute_url_without_barcode():
    area = BusinessArea.objects.first()
    cat = Category.objects.first()
    item = Item.objects.create(
        name="Cable spool",
        business_area=area,
        category=cat,
    )
    assert item.get_absolute_url() == f"/item/id/{item.pk}/"
