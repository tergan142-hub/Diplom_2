import allure
import requests
from constants import BASE_URL


class ApiClient:
    def __init__(self):
        self.session = requests.Session()

    @allure.step("Создание пользователя: {email}")
    def create_user(self, email, password, name):
        return self.session.post(
            f"{BASE_URL}/auth/register",
            json={"email": email, "password": password, "name": name}
        )

    @allure.step("Логин пользователя: {email}")
    def login_user(self, email, password):
        return self.session.post(
            f"{BASE_URL}/auth/login",
            json={"email": email, "password": password}
        )

    @allure.step("Создание заказа с ингредиентами: {ingredients}")
    def create_order(self, ingredients, token=None):
        headers = {"Authorization": token} if token else {}
        return self.session.post(
            f"{BASE_URL}/orders",
            json={"ingredients": ingredients},
            headers=headers
        )