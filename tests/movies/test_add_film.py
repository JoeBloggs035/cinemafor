import pytest
import logging
from constants import MOVIES_ENDPOINT

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class TestAddFilm:
    def test_add_film(self, film_data, auth_requester):
        """
        Тест на добавление фильма с использованием CustomRequester
        """
        logger.info(f"Отправляем данные фильма: {film_data}")

        # Используем CustomRequester для отправки запроса
        response = auth_requester.send_request(
            method="POST",
            endpoint=MOVIES_ENDPOINT,
            data=film_data,
            expected_status=201,
            need_logging=True
        )

        response_data = response.json()
        logger.info(f"Ответ сервера: {response_data}")

        film_id = response_data.get("id")
        assert film_id is not None, "Идентификатор фильма не найден в ответе"

        logger.info(f"Фильм успешно создан с ID: {film_id}")

        assert response_data["name"] == film_data["name"], \
            f"Заданное имя '{film_data['name']}' не совпадает с полученным '{response_data['name']}'"
        assert response_data["price"] == film_data["price"], \
            f"Заданная стоимость {film_data['price']} не совпадает с полученной {response_data['price']}"

        logger.info("Все проверки пройдены успешно")