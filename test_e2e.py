import json

import pytest

from page_objects.login_page import LoginPage
with open('data/test_e2e.json') as json_file:
    test_data = json.load(json_file)
    test_list = test_data["data"]
@pytest.mark.regression
@pytest.mark.parametrize("test_item",test_list)
def test_e2e(browser_configuration, test_item):
    driver = browser_configuration

    # --- GIVEN ---
    driver.get("https://rahulshettyacademy.com/loginpagePractise/")
    login_page = LoginPage(driver)
    shop_page = login_page.login(test_item["username"], test_item["password"])

    # --- WHEN ---
    shop_page.add_product(test_item["product_name"])
    assert shop_page.get_cart_amount() > 0

    # --- THEN ---
    cart_page = shop_page.go_to_cart()
    checkout_page = cart_page.checkout()
    checkout_page.country_input(test_item["tag"]) \
                        .country_picker(test_item["country"]) \
                        .accept_terms_checkbox() \
                        .submit_order()








