def test_search_5_char_code_navigates_to_item(home_page, item_page):
    home_page.navigate()
    home_page.search_bar.search_by_code("A0001")
    item_page.expect_url(code="A0001")


def test_search_4_char_code_navigates_to_item(home_page, item_page):
    home_page.navigate()
    home_page.search_bar.search_by_code("A001")
    item_page.expect_url(code="A001")


def test_empty_barcode_submit_stays_on_page(home_page):
    home_page.navigate()
    home_page.search_bar.search_by_code("")
    home_page.expect_url()


def test_empty_text_search_stays_on_page(home_page):
    home_page.navigate()
    home_page.search_bar.search_by_text("")
    home_page.expect_url()
