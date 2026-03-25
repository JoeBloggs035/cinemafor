from constants import MOVIES_ENDPOINT, MOVIES_BASE_URL


class TestAddFilm:
    def test_add_film_positive(self, film_data, requester):
        """
        201: Тест на добавление афиши фильма
        """
        response = requester.send_request(
            method="POST",
            base_url=MOVIES_BASE_URL,
            endpoint=MOVIES_ENDPOINT,
            data=film_data,
            expected_status=201,
            need_logging=True
        )

        response_data = response.json()
        film_id = response_data.get("id")
        assert film_id is not None, "Идентификатор фильма не найден в ответе"

        assert response_data["name"] == film_data["name"], \
            f"Заданное имя '{film_data['name']}' не совпадает с полученным '{response_data['name']}'"
        assert response_data["price"] == film_data["price"], \
            f"Заданная стоимость {film_data['price']} не совпадает с полученной {response_data['price']}"
