from selenium.webdriver.common.by import By
from helpers.wait_helper import WaitHelper
from page_objects.cart_page import CartPage
from utils.browser_utils import BrowserUtils
import time


class ShopPage(BrowserUtils):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.product_card = (By.XPATH, "//div[@class = 'card h-100']/div/h4")
        self.add_button = (By.XPATH, "./ancestor::div[@class='card h-100']//button")
        self.shop_link = (By.XPATH, "//a[contains(@href, 'shop')]")
        self.go_to_cart_button = (By.XPATH, "//a[contains(@class, 'btn-primary')]")

    def go_to_cart(self):
        wait = WaitHelper(self.driver)
        wait.wait_for_clickable(self.go_to_cart_button).click()
        return CartPage(self.driver)

    def get_cart_amount(self):
        wait_helper = WaitHelper(self.driver)
        print("DEBUG: Starting wait for text '1' in cart button...")
        from selenium.webdriver.support.wait import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        WebDriverWait(self.driver, 20).until(
            EC.text_to_be_present_in_element(self.go_to_cart_button, "1")
        )
        print("DEBUG: Wait passed! Attempting to read text...")
        time.sleep(1)
        cart_raw_text = self.driver.execute_script("return arguments[0].innerText;",
                                                   self.driver.find_element(*self.go_to_cart_button))

        print(f"DEBUG: Raw text from JS: '{cart_raw_text}'")

        digits = ''.join([item for item in cart_raw_text if item.isdigit()])
        return int(digits) if digits else 0
    # def add_product(self, product_name):
    #     wait = WaitHelper(self.driver)
    #     products = wait.wait_for_visible_all(self.product_card)
    #     for product in products:
    #         if product.text == product_name:
    #             target_button = product.find_element(By.XPATH, "./ancestor::div[@class='card h-100']//button")
    #             target_button.click()
    #             break
    #     return ShopPage(self.driver)



    def get_cart_amount(self):
        wait = WaitHelper(self.driver)
        wait.text_to_be_present_in_element(self.go_to_cart_button, "1")
        cart_amount = wait.wait_for_visible(self.go_to_cart_button).text
        return int(''.join([item for item in cart_amount if item.isdigit()]))