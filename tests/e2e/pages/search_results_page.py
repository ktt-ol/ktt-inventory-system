import re
from urllib.parse import quote

from playwright.sync_api import Locator, Page, expect


class SearchResultsPage:
    def __init__(self, page: Page):
        self._page = page

    def result_link(self, name: str) -> Locator:
        return self._page.locator(".content a", has_text=name)

    def expect_url(self, *, term: str) -> None:
        encoded = re.escape(quote(term, safe=""))
        expect(self._page).to_have_url(
            re.compile(rf"/search/{encoded}/$")
        )
