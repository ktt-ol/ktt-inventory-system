import pytest

from inventory.models import Barcode, Item

pytestmark = pytest.mark.django_db


def test_item_description_urls_are_linked(client, area, category):
    item = Item.objects.create(
        name="Coffee machine",
        description="Manual: https://wiki.space.test/coffee",
        business_area=area,
        category=category,
    )
    Barcode.objects.create(code="T001", item=item)

    response = client.get("/item/T001/")

    assert response.status_code == 200
    content = response.content.decode()
    assert '<a href="https://wiki.space.test/coffee"' in content


def test_item_note_urls_are_linked(client, area, category):
    item = Item.objects.create(
        name="3D Printer",
        note="Guide: https://wiki.space.test/3dprint",
        business_area=area,
        category=category,
    )
    Barcode.objects.create(code="T002", item=item)

    response = client.get("/item/T002/")

    assert response.status_code == 200
    content = response.content.decode()
    assert '<a href="https://wiki.space.test/3dprint"' in content


def test_item_by_id_redirects_when_barcode_exists(client, item):
    response = client.get(f"/item/id/{item.pk}/")
    assert response.status_code == 302
    assert response["Location"] == "/item/T0001/"


def test_item_by_id_renders_when_no_barcode(client, item_without_barcode):
    response = client.get(f"/item/id/{item_without_barcode.pk}/")
    assert response.status_code == 200
    assert "Unlabeled item" in response.content.decode()


def test_item_by_id_returns_404_for_missing_item(client):
    response = client.get("/item/id/99999/")
    assert response.status_code == 404


def test_parent_without_barcode_shows_no_brackets(client, item, item_without_barcode):
    item.parent = item_without_barcode
    item.save()

    response = client.get("/item/T0001/")

    content = response.content.decode()
    assert "Unlabeled item" in content
    assert "Unlabeled item []" not in content
