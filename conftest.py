import pytest
import allure
from api.api_client import ApiClient
from helpers.data_generator import generate_email, generate_password, generate_name


@pytest.fixture
def client():
    return ApiClient()


@pytest.fixture
def unique_user(client):
    email = generate_email()
    password = generate_password()
    name = generate_name()
    client.create_user(email, password, name)
    return {"email": email, "password": password, "name": name}


@pytest.fixture
def auth_token(client, unique_user):
    response = client.login_user(unique_user["email"], unique_user["password"])
    return response.json()["accessToken"]