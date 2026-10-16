import pytest

from pages import HomePage, ItemPage


@pytest.fixture
def home_page(page) -> HomePage:
    return HomePage(page)


@pytest.fixture
def item_page(page) -> ItemPage:
    return ItemPage(page)
