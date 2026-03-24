import pytest
import logging
from constants import BASE_URL, MOVIES_ENDPOINT

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class TestBookings:
    def test_add_film(self, film_data, auth_session):
        logger.info(f"Отправляем данные фильма: {film_data}")

        add_film = auth_session.post(f"https://api.dev-cinescope.coconutqa.ru/movies", json=film_data)

        # Логируем ответ сервера
        logger.info(f"Статус ответа: {add_film.status_code}")
        logger.info(f"Тело ответа: {add_film.json()}")

        assert add_film.status_code == 201, f"Ошибка при добавлении фильма. Статус: {add_film.status_code}, Ответ: {add_film.text}"

        film_id = add_film.json().get("id")
        assert film_id is not None, "Идентификатор фильма не найден в ответе"

        logger.info(f"Фильм успешно создан с ID: {film_id}")
        logger.info(f"Созданный фильм: {add_film.json()}")

        assert add_film.json()["name"] == film_data[
            "name"], f"Заданное имя '{film_data['name']}' не совпадает с полученным '{add_film.json()['name']}'"
        assert add_film.json()["price"] == film_data[
            "price"], f"Заданная стоимость {film_data['price']} не совпадает с полученной {add_film.json()['price']}"

        logger.info("Все проверки пройдены успешно")