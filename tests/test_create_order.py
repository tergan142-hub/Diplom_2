import allure

from constants import VALID_INGREDIENTS, INVALID_INGREDIENT


@allure.epic("Stellar Burgers API")
@allure.feature("Создание заказа")
class TestCreateOrder:

    @allure.story("С авторизацией")
    @allure.title("Создание заказа с авторизацией и ингредиентами")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_order_with_auth_and_ingredients(self, client, auth_token):
        response = client.create_order(VALID_INGREDIENTS, token=auth_token)
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "order" in response.json()

    @allure.story("Без авторизации")
    @allure.title("Создание заказа без авторизации")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_order_without_auth(self, client):
        response = client.create_order(VALID_INGREDIENTS)
        assert response.status_code == 401
        assert response.json()["success"] is False
        assert response.json()["message"] == "You should be authorised"

    @allure.story("Без ингредиентов")
    @allure.title("Создание заказа без ингредиентов")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_order_without_ingredients(self, client, auth_token):
        response = client.create_order([], token=auth_token)
        assert response.status_code == 400
        assert response.json()["message"] == "Ingredient ids must be provided"

    @allure.story("Неверный хеш")
    @allure.title("Создание заказа с неверным хешем ингредиентов")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_order_with_invalid_ingredient_hash(self, client, auth_token):
        response = client.create_order([INVALID_INGREDIENT], token=auth_token)
        assert response.status_code == 500