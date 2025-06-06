import pytest
import allure
from pages.main_page import MainPage
from pages.order_page import OrderPage
from datetime import datetime, timedelta

@allure.suite("Тесты сценария заказа самоката")
class TestOrderScooter:
    # Два набора данных для параметризации
    ORDER_DATA = [
        {
            "entry_point": "top",
            "name": "Иван",
            "surname": "Иванов",
            "address": "Пушкина, 10",
            "metro_station": "Сокольники",
            "phone": "89001234567",
            "rental_period": "сутки",
            "color": "черный",
            "comment": "Позвонить за 10 минут"
        },
        {
            "entry_point": "bottom",
            "name": "Мария",
            "surname": "Петрова",
            "address": "Ленина, 25",
            "metro_station": "Лубянка",
            "phone": "89123456789",
            "rental_period": "двое суток",
            "color": "серый",
            "comment": ""
        }
    ]

    @allure.title("Проверка успешного заказа самоката с разными данными и точками входа")
    @pytest.mark.parametrize("order_info", ORDER_DATA)
    def test_successful_scooter_order(self, driver, order_info):
        main_page = MainPage(driver)
        order_page = OrderPage(driver)

        # Выбор точки входа
        allure.attach(f"Точка входа: {order_info['entry_point']}", name="Точка входа заказа", attachment_type=allure.attachment_type.TEXT)
        main_page.click_order_button(order_info["entry_point"])

        # Заполнение первой части формы
        allure.step("Заполнение первой части формы заказа")
        order_page.fill_personal_info(
            order_info["name"],
            order_info["surname"],
            order_info["address"],
            order_info["metro_station"],
            order_info["phone"]
        )

        # Расчет даты доставки (завтра)
        delivery_date = (datetime.now() + timedelta(days=1)).strftime("%d.%m.%Y")

        # Заполнение второй части формы
        allure.step("Заполнение второй части формы заказа")
        order_page.fill_rent_info(
            delivery_date,
            order_info["rental_period"],
            order_info["color"],
            order_info["comment"]
        )

        # Подтверждение заказа
        allure.step("Подтверждение заказа")
        order_page.confirm_order()

        # Проверка всплывающего окна
        allure.step("Проверка всплывающего окна успешного заказа")
        success_message = order_page.get_order_success_message()
        assert "Заказ оформлен" in success_message
        allure.attach(f"Сообщение об успешном заказе: '{success_message}'", name="Сообщение об успехе", attachment_type=allure.attachment_type.TEXT)