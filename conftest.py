from faker import Faker
import pytest
import random
import requests

from api.api_manager import ApiManager
from constants import AUTH_BASE_URL, REGISTER_ENDPOINT, LOGIN_ENDPOINT, HEADERS
from custom_requester.custom_requester import CustomRequester
from entities.user import User
from enums.roles import Roles
from models.base_models import TestUser
from resources.user_creds import SuperAdminCreds
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
        "genreId": random.choice([1, 2, 3, 4, 7, 8, 9, 10])
    }


@pytest.fixture
def test_user() -> TestUser:
    random_password = DataGenerator.generate_random_password()

    return TestUser(
        email=DataGenerator.generate_random_email(),
        fullName=DataGenerator.generate_random_name(),
        password=random_password,
        passwordRepeat=random_password,
        roles=[Roles.USER.value]
    )

@pytest.fixture(scope="function")
def registration_user_data() -> TestUser:
    random_password = DataGenerator.generate_random_password()
    return TestUser(
        email=DataGenerator.generate_random_email(),
        fullName=DataGenerator.generate_random_name(),
        password=random_password,
        passwordRepeat=random_password,
        roles=[Roles.USER.value]
    )


@pytest.fixture(scope="function")
def creation_user_data(test_user):
    """Create a copy of test_user with verified and banned set."""
    # Create a dictionary from the test_user model
    user_dict = test_user.model_dump()

    # Update with additional fields
    user_dict.update({
        "verified": True,
        "banned": False
    })

    # Return the dictionary (or create a new TestUser instance if needed)
    return user_dict


@pytest.fixture(scope="function")
def registered_user(requester, test_user):
    """
    Фикстура для регистрации и получения данных зарегистрированного пользователя.
    """
    # Convert Pydantic model to dict for JSON serialization
    user_dict = test_user.model_dump()

    response = requester.send_request(
        method="POST",
        base_url=AUTH_BASE_URL,
        endpoint=REGISTER_ENDPOINT,
        data=user_dict,  # Use dict instead of model
        expected_status=201
    )
    response_data = response.json()

    # Return a dictionary with user data and credentials
    return {
        "id": response_data["id"],
        "email": test_user.email,
        "password": test_user.password
    }



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

@pytest.fixture(scope="session")
def session():
    """
    Фикстура для создания HTTP-сессии.
    """
    http_session = requests.Session()
    yield http_session
    http_session.close()

@pytest.fixture(scope="session")
def api_manager(session):
    """
    Фикстура для создания экземпляра ApiManager.
    """
    return ApiManager(session)

@pytest.fixture
def user_session():
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()

@pytest.fixture
def super_admin(user_session):
    new_session = user_session()

    super_admin = User(
        SuperAdminCreds.USERNAME,
        SuperAdminCreds.PASSWORD,
        list(Roles.SUPER_ADMIN.value),
        new_session)

    super_admin.api.auth_api.authenticate(super_admin.creds)
    return super_admin

@pytest.fixture
def admin(user_session, super_admin, creation_user_data):
    new_session = user_session()

    admin = User(
        creation_user_data['email'],  # Now works with dict
        creation_user_data['password'],
        list(Roles.ADMIN.value),
        new_session)

    super_admin.api.user_api.create_user(creation_user_data)
    admin.api.auth_api.authenticate(admin.creds)
    return admin

@pytest.fixture
def common_user(user_session, super_admin, creation_user_data):
    new_session = user_session()

    common_user = User(
        creation_user_data['email'],
        creation_user_data['password'],
        list(Roles.USER.value),
        new_session)

    super_admin.api.user_api.create_user(creation_user_data)
    common_user.api.auth_api.authenticate(common_user.creds)
    return common_user