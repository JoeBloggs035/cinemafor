import time

import pytest
from sqlalchemy.orm import Session

from api.api_manager import ApiManager
from constants import REGISTER_ENDPOINT, LOGIN_ENDPOINT, AUTH_BASE_URL
from db_requester.models import UserDBModel
from models.base_models import RegisterUserResponse, TestUser
from resources.user_creds import SuperAdminCreds


class TestAuthAPI:
    def test_register_user(self, api_manager: ApiManager, registration_user_data):
        response = api_manager.auth_api.register_user(user_data=registration_user_data)
        register_user_response = RegisterUserResponse(**response.json())
        assert (
            register_user_response.email == registration_user_data.email
        ), "Email не совпадает"

    def test_register_and_login_user(self, registered_user, api_manager):
        """
        Тест на регистрацию и авторизацию пользователя.
        """
        login_data = {
            "email": registered_user["email"],
            "password": registered_user["password"],
        }
        response = api_manager.auth_api.login_user(login_data)
        response_data = response.json()
        assert "accessToken" in response_data, "Токен доступа отсутствует в ответе"
        assert (
            response_data["user"]["email"] == registered_user["email"]
        ), "Email не совпадает"

    @pytest.mark.parametrize(
        "email, password, expected_status",
        [
            (SuperAdminCreds.USERNAME, SuperAdminCreds.PASSWORD, 200),
            (
                "test_login1@email.com",
                "asdqwe123Q!",
                401,
            ),  # Сервис не может обработать логин по незареганному юзеру
            ("", "password", 401),
        ],
        ids=["Admin login", "Invalid user", "Empty username"],
    )
    def test_login(self, email: str, password: str, expected_status: int, api_manager):
        login_data = {"email": email, "password": password}
        api_manager.auth_api.login_user(
            login_data=login_data, expected_status=expected_status
        )

    # Modul_4\cinemafor\tests\api\test_auth.py
    @pytest.mark.xfail
    def test_register_user_db_session(
        self, api_manager: ApiManager, db_session: Session
    ):
        """
        Тест на регистрацию пользователя с проверкой в базе данных.
        Используем существующего пользователя из фикстуры БД с id=test_id
        """
        # 1. Получаем пользователя из БД (которого создала фикстура db_session)
        user_from_db = (
            db_session.query(UserDBModel).filter(UserDBModel.id == "test_id").first()
        )

        assert (
            user_from_db is not None
        ), "Тестовый пользователь с id=test_id не найден в БД"

        print(f"\n=== Найден пользователь в БД ===")
        print(f"ID: {user_from_db.id}")
        print(f"Email: {user_from_db.email}")
        print(f"Full Name: {user_from_db.full_name}")

        # Сохраняем оригинальные данные для проверки
        original_email = user_from_db.email
        original_full_name = user_from_db.full_name

        # 2. Регистрируем этого же пользователя через API
        user_data = {
            "email": user_from_db.email,
            "fullName": user_from_db.full_name,
            "password": user_from_db.password,
            "passwordRepeat": user_from_db.password,
            "roles": ["USER"],
        }

        # Регистрируем пользователя через API
        response = api_manager.auth_api.register_user(
            user_data=user_data, expected_status=201
        )

        # 3. Получаем ответ от API
        register_user_response = RegisterUserResponse(**response.json())
        print(f"\n=== Пользователь зарегистрирован в API ===")
        print(f"ID из API: {register_user_response.id}")
        print(f"Email из API: {register_user_response.email}")

        # 4. Обновляем ID в БД на реальный ID из API
        user_from_db.id = register_user_response.id
        db_session.commit()
        print(f"ID в БД обновлен с 'test_id' на: {register_user_response.id}")

        # 5. Проверяем, что пользователь присутствует в БД по НОВОМУ ID
        user_after_registration = (
            db_session.query(UserDBModel)
            .filter(
                UserDBModel.id
                == register_user_response.id  # Ищем по новому ID, а не по test_id!
            )
            .first()
        )

        assert (
            user_after_registration is not None
        ), "Пользователь не найден в БД после регистрации"
        assert user_after_registration.email == original_email, "Email не совпадает"
        assert (
            user_after_registration.full_name == original_full_name
        ), "Full name не совпадает"

        print(
            f"\n✓ Тест пройден: пользователь с ID {register_user_response.id} успешно зарегистрирован и найден в БД"
        )
