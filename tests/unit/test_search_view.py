import pytest

from inventory.models import BusinessArea, Category, Item

pytestmark = pytest.mark.django_db


def test_search_empty(client):
    response = client.get("/search/test/")
    assert response.status_code == 200


def test_search_links_item_without_barcode(client):
    area = BusinessArea.objects.first()
    cat = Category.objects.first()
    item = Item.objects.create(
        name="Unique widget",
        business_area=area,
        category=cat,
    )
    response = client.get("/search/Unique/")
    content = response.content.decode()
    assert f"/item/id/{item.pk}/" in content
