import os
import shutil

import pytest

from pages import HomePage, ItemPage


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    chromium = os.environ.get(
        "PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH",
        shutil.which("chromium"),
    )
    if chromium:
        return {**browser_type_launch_args, "executable_path": chromium}
    return browser_type_launch_args


@pytest.fixture
def home_page(page) -> HomePage:
    return HomePage(page)


@pytest.fixture
def item_page(page) -> ItemPage:
    return ItemPage(page)
