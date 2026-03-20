import pytest
from constants import BASE_URL

class TestBookings:
    def test_add_film(self, auth_session, film_data):
        # добавляем фильм
        add_film = auth_session.post(f"{BASE_URL}/movies", json=film_data)
        assert add_film.status_code == 201, "Ошибка при добавлении фильма"

        film_id = add_film.json().get("id")
        assert film_id is not None, "Идентификатор фильма не найден в ответе"
        print(add_film.json())
        print(add_film.json()["name"])
        print(film_data["name"])
        assert add_film.json()["name"] == film_data["name"], "Заданное имя не совпадает"
        assert add_film.json()["price"] == film_data["price"], "Заданная стоимость не совпадает"

        # Проверяем, что бронирование можно получить по ID
        # get_booking = auth_session.get(f"{BASE_URL}/booking/{film_id}")
        # assert get_booking.status_code == 200, "Бронь не найдена"
        # assert get_booking.json()["lastname"] == film_data["lastname"], "Заданная фамилия не совпадает"