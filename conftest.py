import pytest
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager # Для Firefox

@pytest.fixture(scope='function')
def driver():
    # Инициализация драйвера Firefox
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    driver.maximize_window() # Разворачиваем окно браузера
    yield driver
    driver.quit() # Закрываем браузер после выполнения теста