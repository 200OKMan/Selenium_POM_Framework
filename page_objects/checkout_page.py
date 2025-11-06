from selenium.webdriver.common.by import By
from helpers.wait_helper import WaitHelper
from utils.browser_utils import BrowserUtils


class CheckoutPage(BrowserUtils):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.text_field = (By.ID, "country")
        self.countries_list = (By.XPATH, "//div[@class='suggestions']/ul/li/a")
        self.checkbox = (By.XPATH, "//div[@class='checkbox checkbox-primary']")
        self.submit_button = (By.XPATH,"//input[@type='submit']")



    def country_input(self, key):
        wait = WaitHelper(self.driver)
        wait.wait_for_visible(self.text_field).send_keys(key)
        return self

    def country_picker(self, country):
        wait = WaitHelper(self.driver)
        countries = wait.wait_for_visible_all(self.countries_list)
        for item in countries:
            if item.text == country:
                item.click()
                break
        return self

    def accept_terms_checkbox(self):
        wait = WaitHelper(self.driver)
        wait.wait_for_visible(self.checkbox).click()
        return self

    def submit_order(self):
        wait = WaitHelper(self.driver)
        wait.wait_for_visible(self.submit_button).click()
        return self


    # # wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='checkbox checkbox-primary']"))).click()
    # # driver.find_element(By.XPATH,"//input[@type='submit']").click()
    #
    # time.sleep(5)

    # driver.close()