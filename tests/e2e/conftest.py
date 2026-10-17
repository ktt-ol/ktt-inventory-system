import logging
import os

import pytest

from pages import HomePage, ItemPage


logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """
    Launch args, honouring an explicitly configured browser.

    Set only where Playwright's own browsers cannot run; unset, the
    pinned browser is used.
    """
    executable = os.environ.get("E2E_BROWSER_EXECUTABLE")
    if executable:
        logger.info("Browser from E2E_BROWSER_EXECUTABLE: %s", executable)
        return {**browser_type_launch_args, "executable_path": executable}
    logger.info("Browser pinned by Playwright")
    return browser_type_launch_args


@pytest.fixture
def home_page(page) -> HomePage:
    return HomePage(page)


@pytest.fixture
def item_page(page) -> ItemPage:
    return ItemPage(page)
