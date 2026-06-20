import pytest

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
