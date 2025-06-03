import pytest
import allure
from pages.main_page import MainPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@allure.suite("Тесты навигации по логотипам")
class TestHeaderLinks:
    @allure.title("Проверка перехода на главную страницу Самоката по логотипу")
    def test_scooter_logo_redirects_to_main_page(self, driver):
        main_page = MainPage(driver)
        main_page.click_scooter_logo()
        # Проверяем, что URL вернулся к главной странице Самоката
        assert main_page.get_current_url() == MainPage.URL

    @allure.title("Проверка перехода на главную страницу Дзена по логотипу Яндекса")
    def test_yandex_logo_redirects_to_zen_page(self, driver):
        main_page = MainPage(driver)
        initial_url = main_page.get_current_url()
        main_page.click_yandex_logo()

        # Ожидаем нового окна и переключаемся на него
        WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
        driver.switch_to.window(driver.window_handles[1])

        # Ожидаем загрузки страницы Дзена и проверяем URL
        WebDriverWait(driver, 10).until(EC.url_contains("dzen.ru"))
        assert "dzen.ru" in driver.current_url

        # Закрываем вкладку с Дзеном и возвращаемся на исходную вкладку
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        assert driver.current_url == initial_url # Убедимся, что вернулись на главную Самоката