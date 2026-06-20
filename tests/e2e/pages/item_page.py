from playwright.sync_api import Page


class ItemPage:
    def __init__(self, page: Page):
        self._page = page
        self.name = page.locator(".content h1")
