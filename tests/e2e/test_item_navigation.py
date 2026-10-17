from playwright.sync_api import expect

E2E_ITEM_WITHOUT_BARCODE = "E2E Unlabeled Box"


def test_search_navigates_to_item_without_barcode(
    home_page, search_results_page, item_page,
):
    home_page.navigate()
    home_page.search_bar.search_by_text(E2E_ITEM_WITHOUT_BARCODE)

    search_results_page.expect_url(term=E2E_ITEM_WITHOUT_BARCODE)
    search_results_page.result_link(E2E_ITEM_WITHOUT_BARCODE).click()

    item_page.expect_url_by_id()
    expect(item_page.name).to_have_text(E2E_ITEM_WITHOUT_BARCODE)
