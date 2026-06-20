import re

from playwright.sync_api import expect


def test_maxlength_allows_5_char_codes(home_page):
    home_page.navigate()
    expect(home_page.search_bar.barcode_input).to_have_attribute(
        "maxlength", re.compile(r"^[5-9]|[1-9]\d+$"),
    )


def test_search_5_char_code_navigates_to_item(page, home_page):
    home_page.navigate()
    home_page.search_bar.search_by_code("A0001")
    expect(page).to_have_url(re.compile(r"/item/A0001/$"))


def test_search_4_char_code_navigates_to_item(page, home_page):
    home_page.navigate()
    home_page.search_bar.search_by_code("A001")
    expect(page).to_have_url(re.compile(r"/item/A001/$"))
