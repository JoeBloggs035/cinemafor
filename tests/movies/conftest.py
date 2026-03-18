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
    published = faker.random.choice(["true", "false", "--"]) # вообще пофиг что писать
    genre_id = faker.random_int(min=1, max=10)
    created_at = faker.random.choice(["asc", "desc"])
    get_params = f"?pageSize={page_size}&page={page}&minPrice={min_price}&maxPrice={max_price}&locations={locations}&published={published}&genreId={genre_id}&createdAt={created_at}"
    return get_params

@pytest.fixture
def get_film_posters_negative():
    page = 0
    page =  922337203685477568 # меньше чем 1 и больше чем 922337203685477567 - неверные параметры
    page = 1.5
    page = "qwerty"
    page = None
    page = [2, 1, 4, 7, 4, 8, 3, 6, 4, 8]
    min_price = -1  # faker.random_int(min=1, max=2147483647) # если < 0 или min_price > max_price
    min_price = (faker.random_int(min=min_price, max=2147483646))
    max_price = (min_price - 1) #faker.random_int(min=min_price, max=2147483647)# если max_price > 2147483647
    max_price = 2147483648
    locations = 1 # если locations не MSK SPB MSK,SPB
    locations = 1.5
    locations = "1"
    # published = faker.random.choice(["true", "false", 1, 0]) # вообще пофиг что писать
    genre_id =  faker.random_int(min=1, max=10) # меньше 0 и больше 2147483647, str, float, массивы
    created_at = faker.random.choice(["asc", "desc"]) # всё кроме asc и desc
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


