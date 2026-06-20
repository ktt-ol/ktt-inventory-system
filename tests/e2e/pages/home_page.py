from playwright.sync_api import Page

from pages.search_bar import SearchBar


class HomePage:
    def __init__(self, page: Page):
        self._page = page
        self.search_bar = SearchBar(page)

    def navigate(self) -> None:
        self._page.goto("/")
