from selenium.webdriver.common.by import By

from helpers.wait_helper import WaitHelper
from page_objects.cart_page import CartPage
from utils.browser_utils import BrowserUtils


class ShopPage(BrowserUtils):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.product_card = (By.XPATH, "//div[@class = 'card h-100']/div/h4")
        self.add_button = (By.XPATH, "//div[@class ='card-footer']/button")
        # self.product_name = "Blackberry"
        self.shop_link = (By.XPATH, "//a[contains(@href, 'shop')]")
        self.go_to_cart_button = (By.XPATH, "//a[contains(@class, 'btn-primary')]")

    def go_to_cart(self):
        wait = WaitHelper(self.driver)
        wait.wait_for_clickable(self.go_to_cart_button).click()
        return CartPage(self.driver)

    def add_product(self, product_name):
        wait = WaitHelper(self.driver)
        products = wait.wait_for_visible_all(self.product_card, 20)
        for product in products:
            if product.text == product_name:
                wait.wait_for_clickable(self.add_button).click()
        return ShopPage(self.driver)

    def get_cart_amount(self):
        wait = WaitHelper(self.driver)
        cart_amount = wait.wait_for_visible(self.go_to_cart_button).text
        return int(''.join([item for item in cart_amount if item.isdigit()]))