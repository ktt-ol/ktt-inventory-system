import re

from playwright.sync_api import Page, expect


class ItemPage:
    def __init__(self, page: Page):
        self._page = page
        self.name = page.locator(".content h1")

    def expect_url(self, *, code: str) -> None:
        expect(self._page).to_have_url(
            re.compile(rf"/item/{re.escape(code)}/$")
        )

    def expect_url_by_id(self) -> None:
        expect(self._page).to_have_url(
            re.compile(r"/item/id/\d+/$")
        )
