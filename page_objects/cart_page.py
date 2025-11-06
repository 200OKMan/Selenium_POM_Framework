from selenium.webdriver.common.by import By
from helpers.wait_helper import WaitHelper
from page_objects.checkout_page import CheckoutPage
from utils.browser_utils import BrowserUtils


class CartPage(BrowserUtils):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.checkout_button = (By.XPATH, "//button[contains(@class, 'btn-success')]")



    def checkout(self):
        wait = WaitHelper(self.driver)
        wait.wait_for_visible(self.checkout_button, 20).click()
        return CheckoutPage(self.driver)
