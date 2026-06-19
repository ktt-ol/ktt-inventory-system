import re

import pytest
from playwright.sync_api import expect


BARCODE_INPUT = "#itemchooser input[name='id']"


def test_maxlength_allows_5_char_codes(page):
    page.goto("/")
    input_el = page.locator(BARCODE_INPUT)
    expect(input_el).to_have_attribute(
        "maxlength", re.compile(r"^[5-9]|[1-9]\d+$"),
    )


def test_search_5_char_code_navigates_to_item(page):
    page.goto("/")
    page.locator(BARCODE_INPUT).fill("A0001")
    page.locator(BARCODE_INPUT).press("Enter")
    expect(page).to_have_url(re.compile(r"/item/A0001/$"))


def test_search_4_char_code_navigates_to_item(page):
    page.goto("/")
    page.locator(BARCODE_INPUT).fill("A001")
    page.locator(BARCODE_INPUT).press("Enter")
    expect(page).to_have_url(re.compile(r"/item/A001/$"))
