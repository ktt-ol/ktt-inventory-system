from django.test import TestCase

from inventory.models import (
    AcquisitionType,
    Barcode,
    BusinessArea,
    Category,
    Item,
)


class StatsViewTest(TestCase):
    def test_stats_empty_database(self):
        response = self.client.get("/stats/")
        self.assertEqual(response.status_code, 200)

    def test_stats_with_data(self):
        area = BusinessArea.objects.create(name="ideell")
        cat = Category.objects.create(name="Inventar")
        item_a = Item.objects.create(
            name="Soldering iron",
            business_area=area,
            category=cat,
        )
        item_b = Item.objects.create(
            name="Multimeter",
            business_area=area,
            category=cat,
        )
        Barcode.objects.create(code="A0001", item=item_a)
        Barcode.objects.create(code="A0002", item=item_a)
        Barcode.objects.create(code="B0001", item=item_b)

        response = self.client.get("/stats/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["number_of_codes"], 3)
        self.assertEqual(response.context["number_of_items"], 2)
        self.assertEqual(
            response.context["max_barcodes_item"].name,
            "Soldering iron",
        )


class HomeViewTest(TestCase):
    def test_home_empty_database(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)


class GraphViewTest(TestCase):
    def test_graph_empty_database(self):
        response = self.client.get("/graph/")
        self.assertEqual(response.status_code, 200)


class SearchViewTest(TestCase):
    def test_search_empty_database(self):
        response = self.client.get("/search/test/")
        self.assertEqual(response.status_code, 200)
