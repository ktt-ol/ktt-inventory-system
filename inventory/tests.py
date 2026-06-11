from django.test import TestCase


class StatsViewTest(TestCase):
    def test_stats_empty_database(self):
        response = self.client.get("/stats/")
        self.assertEqual(response.status_code, 200)
