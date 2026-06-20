from django.core.management.base import BaseCommand

from inventory.models import Barcode, BusinessArea, Category, Item


class Command(BaseCommand):
    help = "Ensure E2E test data exists (idempotent)"

    def handle(self, *args, **options):
        area, _ = BusinessArea.objects.get_or_create(
            name="E2E Area",
        )
        category, _ = Category.objects.get_or_create(
            name="E2E Category",
        )

        item_with, created = Item.objects.get_or_create(
            name="E2E Soldering Iron",
            defaults={
                "business_area": area,
                "category": category,
            },
        )
        self._report("E2E Soldering Iron", created)
        Barcode.objects.get_or_create(
            code="E0001",
            defaults={"item": item_with},
        )

        item_without, created = Item.objects.get_or_create(
            name="E2E Unlabeled Box",
            defaults={
                "business_area": area,
                "category": category,
            },
        )
        self._report("E2E Unlabeled Box", created)

    def _report(self, name, created):
        status = "created" if created else "exists"
        self.stdout.write(f"  {name}: {status}")
