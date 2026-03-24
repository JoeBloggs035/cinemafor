
from faker import Faker
import pytest
import random
import requests
from constants import BASE_URL, REGISTER_ENDPOINT, LOGIN_ENDPOINT, HEADERS
from custom_requester.custom_requester import CustomRequester
from utils.data_generator import DataGenerator

faker = Faker()

@pytest.fixture(scope="function")
def film_data():
    return {
        "name": f"{faker.word().title()} {faker.word().title()}",
        "imageUrl": faker.image_url(),
        "price": faker.random_int(1, 2147483647),
        "description": faker.english_sentence(nb_words=15, variable_nb_words=False)
                      if hasattr(faker, 'english_sentence')
                      else faker.sentence(nb_words=15),
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
    Фикстура для создания экземпляра CustomRequester.
    """
    session = requests.Session()
    return CustomRequester(session=session, base_url=BASE_URL)

@pytest.fixture(scope="session")
def auth_session():
    session = requests.Session()
    session.headers.update(HEADERS)

    response = requests.post(
        f"https://auth.dev-cinescope.coconutqa.ru/login",
        headers=HEADERS,
        json={"email": "api1@gmail.com", "password": "asdqwe123Q"}
    )
    assert response.status_code == 200, "Ошибка авторизации"
    token = response.json().get("accessToken")
    assert token is not None, "В ответе не оказалось токена"

    session.headers.update({"Authorization": f"Bearer {token}"})
    return session


