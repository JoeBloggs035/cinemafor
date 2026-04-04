from constants import MOVIES_ENDPOINT, MOVIES_BASE_URL


class TestAddFilm:
    def test_add_film_positive(self, film_data, super_admin):
        """
        201: Тест на добавление афиши фильма
        """
        response = super_admin.api.movies_api.create_movie(film_data)
        response_data = response.json()
        film_id = response_data.get("id")
        assert film_id is not None, "Идентификатор фильма не найден в ответе"

        assert response_data["name"] == film_data["name"], \
            f"Заданное имя '{film_data['name']}' не совпадает с полученным '{response_data['name']}'"
        assert response_data["price"] == film_data["price"], \
            f"Заданная стоимость {film_data['price']} не совпадает с полученной {response_data['price']}"

    def test_add_film_common_user(self, film_data, common_user):
        """
        403: Тест на добавление афиши фильма обычным пользователем
        """
        common_user.api.movies_api.create_movie(film_data, expected_status=403)
