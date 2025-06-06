import pytest
import allure
from pages.main_page import MainPage


# Больше не нужно импортировать WebDriverWait и EC напрямую
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

@allure.suite("Тесты навигации по логотипам")
class TestHeaderLinks:
    @allure.title("Проверка перехода на главную страницу Самоката по логотипу")
    def test_scooter_logo_redirects_to_main_page(self, driver):
        main_page = MainPage(driver)
        # Убедимся, что тест начинается с главной страницы Самоката
        # main_page.driver.get(main_page.URL) # Если fixture не гарантирует это

        # Получаем текущий URL до клика, чтобы убедиться, что мы вернемся на него (если это логика логотипа)
        # Если логотип Самоката просто обновляет текущую страницу главной, то просто проверяем конечный URL.
        # В данном случае, это просто переход на главную страницу, поэтому прямого сохранения старого URL не требуется,
        # если мы знаем, что целевой URL - это MainPage.URL.

        main_page.click_scooter_logo()

        # Проверяем, что текущий URL соответствует главной странице Самоката
        assert main_page.get_current_url() == MainPage.URL

    @allure.title("Проверка перехода на главную страницу Дзена по логотипу Яндекса")
    def test_yandex_logo_redirects_to_zen_page(self, driver):
        main_page = MainPage(driver)
        # Сохраняем исходный URL и хэндл окна перед кликом
        initial_url = main_page.get_current_url()
        original_window_handle = driver.current_window_handle  # Здесь driver.current_window_handle допустим, т.к. это получение состояния драйвера, а не действие.

        main_page.click_yandex_logo()  # Кликаем по логотипу Яндекса

        # Ожидаем появления нового окна и переключаемся на него через метод BasePage
        # Этот метод вернет хэндл исходного окна, но мы его уже сохранили.
        # Здесь мы могли бы использовать: original_window_handle_from_method = main_page.switch_to_new_window()
        # Для простоты, так как хэндл основного окна уже есть, можно просто вызвать switch_to_new_window
        main_page.switch_to_new_window()

        # Ожидаем, что URL нового окна будет содержать "dzen.ru", используя метод BasePage
        main_page.wait_for_url_contains("dzen.ru")
        assert "dzen.ru" in main_page.get_current_url()  # Используем get_current_url() из BasePage

        # Закрываем текущую вкладку (вкладку Дзена)
        driver.close()  # Прямое закрытие окна через driver допустимо, т.к. это действие с браузером, не с элементом.

        # Возвращаемся на исходную вкладку Самоката, используя метод BasePage
        main_page.switch_to_window_by_handle(original_window_handle)

        # Проверяем, что мы вернулись на исходный URL главной страницы Самоката
        assert main_page.get_current_url() == initial_url