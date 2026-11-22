import pytest
import allure

from constants import BASE_URL
from helpers.data_generator import generate_email, generate_password, generate_name


@allure.epic("Stellar Burgers API")
@allure.feature("Создание пользователя")
class TestCreateUser:

    @allure.story("Уникальный пользователь")
    @allure.title("Создание уникального пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_unique_user(self, client):
        email = generate_email()
        response = client.create_user(email, generate_password(), generate_name())
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "accessToken" in response.json()

    @allure.story("Существующий пользователь")
    @allure.title("Создание пользователя, который уже зарегистрирован")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_existing_user(self, client, unique_user):
        response = client.create_user(
            unique_user["email"], unique_user["password"], unique_user["name"]
        )
        assert response.status_code == 403
        assert response.json()["message"] == "User already exists"

    @allure.story("Обязательные поля")
    @allure.title("Создание пользователя без обязательного поля: {missing_field}")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_required_field(self, client, missing_field):
        data = {"email": generate_email(), "password": generate_password(), "name": generate_name()}
        data.pop(missing_field)
        response = client.session.post(f"{BASE_URL}/auth/register", json=data)
        assert response.status_code == 403
        assert response.json()["message"] == "Email, password and name are required fields"