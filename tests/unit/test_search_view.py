import pytest

pytestmark = pytest.mark.django_db


def test_search_empty(client):
    response = client.get("/search/test/")
    assert response.status_code == 200


def test_search_links_item_without_barcode(client, item_without_barcode):
    response = client.get("/search/Unlabeled/")
    content = response.content.decode()
    assert f"/item/id/{item_without_barcode.pk}/" in content
