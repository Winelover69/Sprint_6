from selenium.webdriver.common.by import By
from .base_page import BasePage

class OrderPage(BasePage):
    # Локаторы для первой страницы формы заказа
    NAME_INPUT = (By.XPATH, ".//input[@placeholder='* Имя']")
    SURNAME_INPUT = (By.XPATH, ".//input[@placeholder='* Фамилия']")
    ADDRESS_INPUT = (By.XPATH, ".//input[@placeholder='* Адрес: куда привезти заказ']")
    METRO_STATION_INPUT = (By.XPATH, ".//input[@placeholder='* Станция метро']")
    PHONE_INPUT = (By.XPATH, ".//input[@placeholder='* Телефон: на него позвонит курьер']")
    NEXT_BUTTON = (By.XPATH, ".//button[text()='Далее']")

    # Локаторы для второй страницы формы заказа
    DELIVERY_DATE_INPUT = (By.XPATH, ".//input[@placeholder='* Когда привезти самокат']")
    RENTAL_PERIOD_DROPDOWN = (By.CLASS_NAME, "Dropdown-placeholder")
    RENTAL_PERIOD_OPTIONS = (By.XPATH, ".//div[contains(@class, 'Dropdown-option')]")
    COLOR_BLACK_RADIO = (By.ID, "black")
    COLOR_GREY_RADIO = (By.ID, "grey")
    COMMENT_INPUT = (By.XPATH, ".//input[@placeholder='Комментарий для курьера']")
    ORDER_BUTTON = (By.XPATH, ".//div[@class='Order_Buttons__1xGrp']/button[text()='Заказать']")
    CONFIRM_ORDER_BUTTON = (By.XPATH, ".//button[text()='Да']")

    # Локатор всплывающего окна успешного заказа
    ORDER_SUCCESS_POPUP = (By.CLASS_NAME, "Order_ModalHeader__3SsAD")

    def fill_personal_info(self, name, surname, address, metro_station, phone):
        self.find_element(self.NAME_INPUT).send_keys(name)
        self.find_element(self.SURNAME_INPUT).send_keys(surname)
        self.find_element(self.ADDRESS_INPUT).send_keys(address)
        self.find_element(self.METRO_STATION_INPUT).send_keys(metro_station)
        # Выбор станции метро из выпадающего списка
        self.click_element((By.XPATH, f".//div[@class='select-search__select']//div[text()='{metro_station}']"))
        self.find_element(self.PHONE_INPUT).send_keys(phone)
        self.click_element(self.NEXT_BUTTON)

    def fill_rent_info(self, delivery_date, rental_period_text, color, comment=""):
        self.find_element(self.DELIVERY_DATE_INPUT).send_keys(delivery_date)
        # Клик по текущей дате в календаре (после ввода даты)
        self.click_element((By.XPATH, ".//div[contains(@class, 'react-datepicker__day--selected')]"))

        self.click_element(self.RENTAL_PERIOD_DROPDOWN)
        # Выбор периода аренды
        self.click_element((self.RENTAL_PERIOD_OPTIONS[0], self.RENTAL_PERIOD_OPTIONS[1] + f"[text()='{rental_period_text}']"))

        if color == "черный":
            self.click_element(self.COLOR_BLACK_RADIO)
        elif color == "серый":
            self.click_element(self.COLOR_GREY_RADIO)

        if comment:
            self.find_element(self.COMMENT_INPUT).send_keys(comment)

        self.click_element(self.ORDER_BUTTON)

    def confirm_order(self):
        self.click_element(self.CONFIRM_ORDER_BUTTON)

    def get_order_success_message(self):
        # Добавим явное ожидание видимости всплывающего окна
        return self.get_element_text(self.ORDER_SUCCESS_POPUP)