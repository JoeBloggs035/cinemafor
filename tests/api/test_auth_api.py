
import pytest

from api.api_manager import ApiManager
from constants import REGISTER_ENDPOINT, LOGIN_ENDPOINT, AUTH_BASE_URL
from models.base_models import RegisterUserResponse
from resources.user_creds import SuperAdminCreds


class TestAuthAPI:
    def test_register_user(self, api_manager: ApiManager, registration_user_data):
        response = api_manager.auth_api.register_user(user_data=registration_user_data)
        register_user_response = RegisterUserResponse(**response.json())
        assert register_user_response.email == registration_user_data.email, "Email не совпадает"

    def test_register_and_login_user(self, registered_user, api_manager):
        """
        Тест на регистрацию и авторизацию пользователя.
        """
        login_data = {
            "email": registered_user["email"],
            "password": registered_user["password"]
        }
        response = api_manager.auth_api.login_user(login_data)
        response_data = response.json()
        assert "accessToken" in response_data, "Токен доступа отсутствует в ответе"
        assert response_data["user"]["email"] == registered_user["email"], "Email не совпадает"

    @pytest.mark.parametrize("email, password, expected_status", [
        (SuperAdminCreds.USERNAME, SuperAdminCreds.PASSWORD, 200),
        ("test_login1@email.com", "asdqwe123Q!", 401),  # Сервис не может обработать логин по незареганному юзеру
        ("", "password", 401),
    ], ids=["Admin login", "Invalid user", "Empty username"])
    def test_login(self, email: str, password: str, expected_status: int, api_manager):
        login_data = {
            "email": email,
            "password": password
        }
        api_manager.auth_api.login_user(login_data=login_data, expected_status=expected_status)
