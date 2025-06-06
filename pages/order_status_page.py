from selenium.webdriver.common.by import By
from .base_page import BasePage

class OrderStatusPage(BasePage):
    ORDER_SUCCESS_POPUP_HEADER = (By.CLASS_NAME, "Order_ModalHeader__3SsAD")
    # Другие локаторы, если нужны (например, кнопка "Посмотреть статус")

    def is_order_success_popup_displayed(self):
        try:
            self.find_element(self.ORDER_SUCCESS_POPUP_HEADER, timeout=5)
            return True
        except TimeoutError:
            return False

    def get_order_success_message(self):
        return self.get_element_text(self.ORDER_SUCCESS_POPUP_HEADER)