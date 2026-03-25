from faker import Faker
import pytest
import random
import requests
from constants import AUTH_BASE_URL, REGISTER_ENDPOINT, LOGIN_ENDPOINT, HEADERS
from custom_requester.custom_requester import CustomRequester
from utils.data_generator import DataGenerator

faker = Faker()


@pytest.fixture(scope="function")
def film_data():
    return {
        "name": DataGenerator.generate_valid_film_title(),
        "imageUrl": faker.image_url(),
        "price": faker.random_int(1, 2147483647),
        "description": DataGenerator.generate_valid_film_description(),
        "location": random.choice(["MSK", "SPB"]),
        "published": random.choice([True, False]),
        "genreId": faker.random_int(min=1, max=10)
    }


@pytest.fixture(scope="function")
def test_user():
    """
    Генерация случайного пользователя для тестов.
    """
    random_email = DataGenerator.generate_random_email()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()

    return {
        "email": random_email,
        "fullName": random_name,
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": ["USER"]
    }


@pytest.fixture(scope="function")
def registered_user(requester, test_user):
    """
    Фикстура для регистрации и получения данных зарегистрированного пользователя.
    """
    response = requester.send_request(
        method="POST",
        base_url=AUTH_BASE_URL,
        endpoint=REGISTER_ENDPOINT,
        data=test_user,
        expected_status=201
    )
    response_data = response.json()
    registered_user = test_user.copy()
    registered_user["id"] = response_data["id"]
    return registered_user



@pytest.fixture(scope="session")
def requester():
    """
    Фикстура для создания авторизованного CustomRequester.
    Получает токен и добавляет его в заголовки.
    """
    # Создаем сессию с заголовками
    session = requests.Session()
    session.headers.update(HEADERS)

    # Получаем токен через отдельный запрос к auth сервису
    auth_url = f"{AUTH_BASE_URL.rstrip('/')}{LOGIN_ENDPOINT}"
    response = session.post(
        auth_url,
        headers=HEADERS,
        json={"email": "api1@gmail.com", "password": "asdqwe123Q"}
    )
    assert response.status_code == 200, f"Ошибка авторизации: {response.status_code} - {response.text}"
    token = response.json().get("accessToken")
    assert token is not None, "В ответе не оказалось токена"

    # Обновляя хедеры создаем авторизованный CustomRequester
    session.headers.update({"Authorization": f"Bearer {token}"})
    return CustomRequester(session=session)
