import allure # Импортируем allure, если еще не импортирован
from selenium.webdriver.common.by import By
from .base_page import BasePage

class MainPage(BasePage):
    URL = "https://qa-scooter.praktikum-services.ru/"

    # Локаторы для раздела "Вопросы о важном"
    ACCORDION_QUESTIONS_LOCATORS = (By.XPATH, ".//div[contains(@class, 'accordion__button')]")
    ACCORDION_ANSWERS_LOCATORS = (By.XPATH, ".//div[contains(@class, 'accordion__panel')]/p")

    # Локаторы кнопок "Заказать"
    ORDER_BUTTON_TOP = (By.CLASS_NAME, "Button_Button__rwUu7")
    ORDER_BUTTON_BOTTOM = (By.XPATH, ".//button[contains(@class, 'Button_Middle__1CSJM') and text()='Заказать']")

    # Локаторы логотипов
    SCOOTER_LOGO = (By.CLASS_NAME, "Header_LogoScooter__3lsAR")
    YANDEX_LOGO = (By.CLASS_NAME, "Header_LogoYandex__3grXM")

    def __init__(self, driver):
        super().__init__(driver)
        self.driver.get(self.URL)

    @allure.step("Кликнуть на вопрос аккордеона по индексу {question_index} и получить текст ответа")
    def click_question_and_get_answer(self, question_index):
        # Чтобы не получать все вопросы снова, можно передать локатор конкретного вопроса
        # Однако, если вопросы динамические, лучше сначала получить все и скроллить к конкретному
        question_locator_for_scroll = (self.ACCORDION_QUESTIONS_LOCATORS[0],
                                        self.ACCORDION_QUESTIONS_LOCATORS[1] + f"[{question_index + 1}]")
        self.scroll_to_element(question_locator_for_scroll) # Используем новый метод скролла из BasePage
        self.click_element(question_locator_for_scroll)

        answer_locator = (self.ACCORDION_ANSWERS_LOCATORS[0],
                          self.ACCORDION_ANSWERS_LOCATORS[1] + f"[{question_index + 1}]")
        # Ждем, пока ответ станет видимым, и получаем его текст
        return self.get_element_text(answer_locator) # Используем метод получения текста из BasePage

    @allure.step("Кликнуть по кнопке 'Заказать' ({location})")
    def click_order_button(self, location="top"):
        if location == "top":
            self.click_element(self.ORDER_BUTTON_TOP)
        elif location == "bottom":
            self.scroll_to_element(self.ORDER_BUTTON_BOTTOM) # Используем новый метод скролла
            self.click_element(self.ORDER_BUTTON_BOTTOM)
        else:
            raise ValueError("Некорректное значение 'location'. Допустимо 'top' или 'bottom'.")

    @allure.step("Кликнуть по логотипу Самоката")
    def click_scooter_logo(self):
        self.click_element(self.SCOOTER_LOGO)

    @allure.step("Кликнуть по логотипу Яндекса")
    def click_yandex_logo(self):
        self.click_element(self.YANDEX_LOGO)