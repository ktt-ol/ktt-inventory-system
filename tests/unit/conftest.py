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


@pytest.fixture
def area(db):
    """First BusinessArea from baseline data."""
    return BusinessArea.objects.first()


@pytest.fixture
def category(db):
    """First Category from baseline data."""
    return Category.objects.first()


@pytest.fixture
def item(db, area, category):
    """Item with a barcode."""
    obj = Item.objects.create(
        name="Test item",
        business_area=area,
        category=category,
    )
    Barcode.objects.create(code="T0001", item=obj)
    return obj


@pytest.fixture
def item_without_barcode(db, area, category):
    """Item without any barcode."""
    return Item.objects.create(
        name="Unlabeled item",
        business_area=area,
        category=category,
    )


@pytest.fixture
def item_with_short_code(db, area, category):
    """Item whose code is shorter than the default range addresses."""
    obj = Item.objects.create(
        name="SD cards",
        business_area=area,
        category=category,
    )
    Barcode.objects.create(code="M01", item=obj)
    return obj
