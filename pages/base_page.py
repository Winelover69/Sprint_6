import allure # Импортируем allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement

class BasePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    @allure.step("Найти элемент по локатору {locator} с таймаутом {timeout} секунд")
    def find_element(self, locator, timeout=10):
        try:
            return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            allure.attach(f"Элемент с локатором {locator} не найден за {timeout} секунд.", name="Ошибка поиска элемента", attachment_type=allure.attachment_type.TEXT)
            raise TimeoutError(f"Элемент с локатором {locator} не найден за {timeout} секунд.")

    @allure.step("Найти все элементы по локатору {locator} с таймаутом {timeout} секунд")
    def find_elements(self, locator, timeout=10):
        try:
            return WebDriverWait(self.driver, timeout).until(EC.visibility_of_all_elements_located(locator))
        except TimeoutException:
            allure.attach(f"Элементы с локатором {locator} не найдены за {timeout} секунд.", name="Ошибка поиска элементов", attachment_type=allure.attachment_type.TEXT)
            raise TimeoutError(f"Элементы с локатором {locator} не найдены за {timeout} секунд.")

    @allure.step("Кликнуть по элементу с локатором {locator}")
    def click_element(self, locator, timeout=10):
        element = self.find_element(locator, timeout)
        element.click()
        allure.attach(f"Клик по элементу: {locator}", name="Действие", attachment_type=allure.attachment_type.TEXT)

    @allure.step("Получить текущий URL")
    def get_current_url(self):
        url = self.driver.current_url
        allure.attach(f"Текущий URL: {url}", name="Информация", attachment_type=allure.attachment_type.TEXT)
        return url

    @allure.step("Получить текст элемента по локатору {locator}")
    def get_element_text(self, locator, timeout=10):
        element_text = self.find_element(locator, timeout).text
        allure.attach(f"Текст элемента {locator}: '{element_text}'", name="Информация", attachment_type=allure.attachment_type.TEXT)
        return element_text

    @allure.step("Ожидать изменения URL с {old_url} на новый")
    def wait_for_url_change(self, old_url, timeout=10):
        WebDriverWait(self.driver, timeout).until(EC.url_changes(old_url))
        allure.attach(f"URL изменился с '{old_url}' на '{self.driver.current_url}'", name="Информация", attachment_type=allure.attachment_type.TEXT)

    @allure.step("Проскроллить до элемента по локатору {locator}")
    def scroll_to_element(self, locator, timeout=10):
        element = self.find_element(locator, timeout)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        allure.attach(f"Проскроллено до элемента: {locator}", name="Действие", attachment_type=allure.attachment_type.TEXT)

    # --- Новые методы для работы с окнами ---
    @allure.step("Ожидать появления нового окна и переключиться на него")
    def switch_to_new_window(self, timeout=10):
        """
        Ожидает появления второго окна и переключается на него.
        Возвращает хэндл исходного окна, чтобы можно было вернуться.
        """
        original_window_handle = self.driver.current_window_handle
        WebDriverWait(self.driver, timeout).until(EC.number_of_windows_to_be(2))
        for window_handle in self.driver.window_handles:
            if window_handle != original_window_handle:
                self.driver.switch_to.window(window_handle)
                allure.attach(f"Переключено на новое окно. Хэндл: {window_handle}", name="Переключение окна", attachment_type=allure.attachment_type.TEXT)
                return original_window_handle # Возвращаем хэндл исходного окна
        raise TimeoutError("Не удалось переключиться на новое окно.")

    @allure.step("Переключиться на окно по заданному хэндлу")
    def switch_to_window_by_handle(self, window_handle):
        """
        Переключается на окно по заданному хэндлу.
        """
        self.driver.switch_to.window(window_handle)
        allure.attach(f"Переключено на окно с хэндлом: {window_handle}", name="Переключение окна", attachment_type=allure.attachment_type.TEXT)

    @allure.step("Ожидать, что текущий URL содержит подстроку '{expected_url_part}'")
    def wait_for_url_contains(self, expected_url_part, timeout=10):
        """
        Ожидает, пока текущий URL браузера не будет содержать указанную подстроку.
        """
        WebDriverWait(self.driver, timeout).until(EC.url_contains(expected_url_part))
        allure.attach(f"URL содержит '{expected_url_part}'. Текущий URL: {self.driver.current_url}", name="Проверка URL", attachment_type=allure.attachment_type.TEXT)