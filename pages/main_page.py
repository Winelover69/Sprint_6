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

    def click_question_and_get_answer(self, question_index):
        questions = self.find_elements(self.ACCORDION_QUESTIONS_LOCATORS)
        # Скроллим до элемента, чтобы он был виден и кликабелен
        self.driver.execute_script("arguments[0].scrollIntoView();", questions[question_index])
        self.click_element((self.ACCORDION_QUESTIONS_LOCATORS[0], self.ACCORDION_QUESTIONS_LOCATORS[1] + f"[{question_index + 1}]"))
        # Теперь получаем текст ответа
        answers = self.find_elements(self.ACCORDION_ANSWERS_LOCATORS)
        # Важно: иногда ответ может появиться не сразу, нужно подождать его видимости
        self.find_element((self.ACCORDION_ANSWERS_LOCATORS[0], self.ACCORDION_ANSWERS_LOCATORS[1] + f"[{question_index + 1}]"))
        return answers[question_index].text

    def click_order_button(self, location="top"):
        if location == "top":
            self.click_element(self.ORDER_BUTTON_TOP)
        elif location == "bottom":
            # Скроллим до нижней кнопки
            self.driver.execute_script("arguments[0].scrollIntoView();", self.find_element(self.ORDER_BUTTON_BOTTOM))
            self.click_element(self.ORDER_BUTTON_BOTTOM)
        else:
            raise ValueError("Некорректное значение 'location'. Допустимо 'top' или 'bottom'.")

    def click_scooter_logo(self):
        self.click_element(self.SCOOTER_LOGO)

    def click_yandex_logo(self):
        self.click_element(self.YANDEX_LOGO)