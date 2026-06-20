import pytest

from inventory.models import Barcode, BusinessArea, Category, Item

pytestmark = pytest.mark.django_db


def test_item_description_urls_are_linked(client):
    area = BusinessArea.objects.first()
    cat = Category.objects.first()
    item = Item.objects.create(
        name="Coffee machine",
        description="Manual: https://wiki.space.test/coffee",
        business_area=area,
        category=cat,
    )
    Barcode.objects.create(code="T001", item=item)

    response = client.get("/item/T001/")

    assert response.status_code == 200
    content = response.content.decode()
    assert '<a href="https://wiki.space.test/coffee"' in content


def test_item_note_urls_are_linked(client):
    area = BusinessArea.objects.first()
    cat = Category.objects.first()
    item = Item.objects.create(
        name="3D Printer",
        note="Guide: https://wiki.space.test/3dprint",
        business_area=area,
        category=cat,
    )
    Barcode.objects.create(code="T002", item=item)

    response = client.get("/item/T002/")

    assert response.status_code == 200
    content = response.content.decode()
    assert '<a href="https://wiki.space.test/3dprint"' in content


def test_item_by_id_redirects_when_barcode_exists(client):
    item = Item.objects.get(name="Soldering iron")
    response = client.get(f"/item/id/{item.pk}/")
    assert response.status_code == 302
    assert response["Location"] == "/item/A0001/"


def test_item_by_id_renders_when_no_barcode(client):
    area = BusinessArea.objects.first()
    cat = Category.objects.first()
    item = Item.objects.create(
        name="Unlabeled box",
        business_area=area,
        category=cat,
    )
    response = client.get(f"/item/id/{item.pk}/")
    assert response.status_code == 200
    assert "Unlabeled box" in response.content.decode()


def test_item_by_id_returns_404_for_missing_item(client):
    response = client.get("/item/id/99999/")
    assert response.status_code == 404
