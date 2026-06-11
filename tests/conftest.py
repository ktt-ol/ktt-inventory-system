import pytest

from django.core.management import call_command

from inventory.models import Barcode, BusinessArea, Category, Item


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    """Populate baseline inventory data for the test session."""
    with django_db_blocker.unblock():
        area = BusinessArea.objects.create(name="Test Area")
        cat = Category.objects.create(name="Test Category")
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


@pytest.fixture
def empty_db(transactional_db):
    """Provide an empty database by flushing all data."""
    call_command("flush", "--no-input", verbosity=0)
