from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

class WaitHelper:
    def __init__(self, driver):
        self.driver = driver


    def wait_for_clickable(self, element, timeout=30):
        return WebDriverWait(self.driver, timeout).until(expected_conditions.element_to_be_clickable(element))

    def wait_for_visible(self, element, timeout=30):
        return WebDriverWait(self.driver, timeout).until(expected_conditions.visibility_of_element_located(element))

    def wait_for_visible_all(self, element, timeout=30):
        return WebDriverWait(self.driver, timeout).until(expected_conditions.visibility_of_all_elements_located(element))

    def text_to_be_present_in_element(self, element, text, timeout=30):
        return WebDriverWait(self.driver, timeout).until(expected_conditions.text_to_be_present_in_element(element, text))

