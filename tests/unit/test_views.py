import pytest

from inventory.models import Barcode, BusinessArea, Category, Item

pytestmark = pytest.mark.django_db


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200


def test_graph(client):
    response = client.get("/graph/")
    assert response.status_code == 200


def test_search_empty(client):
    response = client.get("/search/test/")
    assert response.status_code == 200


def test_stats_with_baseline(client):
    response = client.get("/stats/")
    assert response.status_code == 200
    assert response.context["number_of_codes"] == 3
    assert response.context["number_of_items"] == 2
    max_item = response.context["max_barcodes_item"]
    assert max_item.name == "Soldering iron"
    assert max_item.num_barcodes == 2


def test_stats_empty_database(client, empty_db):
    response = client.get("/stats/")
    assert response.status_code == 200
    assert response.context["number_of_items"] == 0
    assert response.context["max_barcodes_item"] is None


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
