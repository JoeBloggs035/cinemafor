import pytest
import requests
from faker import Faker
from constants import HEADERS, BASE_URL

faker = Faker()


@pytest.fixture(scope="session")
def auth_session():
    session = requests.Session()
    session.headers.update(HEADERS)

    response = requests.post(
        f"{BASE_URL}/auth",
        headers=HEADERS,
        json={"username": "api1@gmail.com", "password": "asdqwe123Q"},
    )
    assert response.status_code == 200, "Ошибка авторизации"
    token = response.json().get("token")
    assert token is not None, "В ответе не оказалось токена"

    session.headers.update({"Cookie": f"token={token}"})
    return session


@pytest.fixture
def get_film_posters():
    page_size = faker.random_int(min=1, max=20)
    page = 1
    min_price = 1  # faker.random_int(min=1, max=2147483647)
    max_price = faker.random_int(min=min_price, max=2147483647)
    locations = faker.random.choice(["MSK", "SPB", "MSK,SPB"])
    published = faker.random.choice(["true", "false", "--"])
    genre_id = faker.random_int(min=1, max=10)
    created_at = faker.random.choice(["asc", "desc"])
    get_params = f"?pageSize={page_size}&page={page}&minPrice={min_price}&maxPrice={max_price}&locations={locations}&published={published}&genreId={genre_id}&createdAt={created_at}"
    return get_params


@pytest.fixture
def put_booking_data():
    return {
        "firstname": faker.first_name(),
        "lastname": faker.last_name(),
        "totalprice": faker.random_int(min=100, max=100000),
        "depositpaid": True,
        "bookingdates": {"checkin": "2024-04-07", "checkout": "2024-04-09"},
        "additionalneeds": faker.word(),
    }


@pytest.fixture
def patch_booking_data():
    return {"firstname": faker.first_name(), "additionalneeds": faker.word()}


@pytest.fixture
def bad_booking_data():
    return {
        "firstname": faker.random_int(
            min=100, max=100000
        ),  # неверный формат данных имени
        "lastname": faker.last_name(),
        "totalprice": faker.first_name(),
        "depositpaid": True,
        "bookingdates": {"checkin": "2024-04-07", "checkout": "2024-04-09"},
        "additionalneeds": faker.word(),
    }
