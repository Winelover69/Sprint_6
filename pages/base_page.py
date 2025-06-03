from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import TimeoutException

class BasePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def find_element(self, locator, timeout=10):
        try:
            return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            raise TimeoutError(f"Элемент с локатором {locator} не найден за {timeout} секунд.")

    def find_elements(self, locator, timeout=10):
        try:
            return WebDriverWait(self.driver, timeout).until(EC.visibility_of_all_elements_located(locator))
        except TimeoutException:
            raise TimeoutError(f"Элементы с локатором {locator} не найдены за {timeout} секунд.")

    def click_element(self, locator, timeout=10):
        element = self.find_element(locator, timeout)
        element.click()

    def get_current_url(self):
        return self.driver.current_url

    def get_element_text(self, locator, timeout=10):
        element = self.find_element(locator, timeout)
        return element.text

    def wait_for_url_change(self, old_url, timeout=10):
        WebDriverWait(self.driver, timeout).until(EC.url_changes(old_url))