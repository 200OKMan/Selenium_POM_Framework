from selenium.webdriver.common.by import By
from page_objects.shop_page import ShopPage
from utils.browser_utils import BrowserUtils


class LoginPage(BrowserUtils):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.username_locator = (By.ID, "username")
        self.password_locator = (By.ID, "password")
        self.login_locator = (By.ID, "signInBtn")


    def login(self, username, password):
        self.driver.find_element(*self.username_locator).send_keys(username)
        self.driver.find_element(*self.password_locator).send_keys(password)
        self.driver.find_element(*self.login_locator).click()
        return ShopPage(self.driver)
