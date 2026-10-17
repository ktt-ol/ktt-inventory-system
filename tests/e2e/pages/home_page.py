import re

from playwright.sync_api import Page, expect

from pages.search_bar import SearchBar


class HomePage:
    URL = "/"

    def __init__(self, page: Page):
        self._page = page
        self.search_bar = SearchBar(page)

    def navigate(self) -> None:
        self._page.goto(self.URL)

    def expect_url(self) -> None:
        expect(self._page).to_have_url(re.compile(r"/$"))
