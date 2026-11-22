import pytest
import allure


@allure.epic("Stellar Burgers API")
@allure.feature("Логин пользователя")
class TestLoginUser:

    @allure.story("Существующий пользователь")
    @allure.title("Вход под существующим пользователем")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_existing_user(self, client, unique_user):
        response = client.login_user(unique_user["email"], unique_user["password"])
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "accessToken" in response.json()

    @allure.story("Неверные данные")
    @allure.title("Вход с неверным логином и паролем: {email}")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("email,password", [
        ("wrong@email.com", "password123"),
        ("correct@email.com", "wrongpassword"),
    ])
    def test_login_invalid_credentials(self, client, email, password):
        response = client.login_user(email, password)
        assert response.status_code == 401
        assert response.json()["message"] == "email or password are incorrect"