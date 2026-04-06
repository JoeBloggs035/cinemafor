# Modul_4\Cinescope\tests\api\test_auth.py
import datetime

from api.api_manager import ApiManager
from enums.roles import Roles
from models.base_models import TestUser, RegisterUserResponse


def test_register_user_mock(api_manager: ApiManager, test_user: TestUser, mocker):
    # Ответ полученный из мок сервиса
    mock_response = RegisterUserResponse(  # Фиктивный ответ
        id="id",
        email="email@email.com",
        fullName="fullName",
        verified=True,
        banned=False,
        roles=[Roles.SUPER_ADMIN],
        createdAt=str(datetime.datetime.now())
    )

    # Мокаем метод register_user в auth_api
    mocker.patch.object(
        api_manager.auth_api,  # Объект, который нужно замокать
        'register_user',  # Метод, который нужно замокать
        return_value=mock_response  # Фиктивный ответ
    )
    # Вызываем метод, который должен быть замокан
    register_user_response = api_manager.auth_api.register_user(test_user)
    # Проверяем, что ответ соответствует ожидаемому
    assert register_user_response.email == mock_response.email, "Email не совпадает"