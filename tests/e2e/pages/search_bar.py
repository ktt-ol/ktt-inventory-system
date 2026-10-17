from playwright.sync_api import Page


class SearchBar:
    def __init__(self, page: Page):
        self.barcode_input = page.locator(
            "#itemchooser input[name='id']"
        )
        self.text_input = page.locator(
            "#itemsearch input[name='term']"
        )

    def search_by_code(self, code: str) -> None:
        self.barcode_input.fill(code)
        self.barcode_input.press("Enter")

    def search_by_text(self, term: str) -> None:
        self.text_input.fill(term)
        self.text_input.press("Enter")
