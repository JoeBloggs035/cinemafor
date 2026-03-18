import requests
import pytest

from conftest import get_film_posters
from constants import BASE_URL


class TestMovies:
    def test_movies_get_positive(self, get_film_posters):
        # Получаем афиши фильмов по параметрам
        film_posters = requests.get(f"{BASE_URL}/movies{get_film_posters}")
        assert film_posters.status_code == 200, "Ошибка при получении афиш фильмов"
        assert "count" in film_posters.json()
        assert "page" in film_posters.json()
        assert "pageSize" in film_posters.json()
        assert "pageCount" in film_posters.json()

    @pytest.mark.parametrize('invalid_parameter', [
        '?pageSize=-1',
        '?pageSize=2147483648',
        '?pageSize="qwerty"',
        '?pageSize=1.5',
        '?pageSize=None',
        '?pageSize=[1, 2, "a"]',
        '?pageSize=(1, 2, "a")',
        '?pageSize={1, 2, "a"}'
    ])

    def test_movies_get_negative(self, invalid_parameter):
        # Получаем афиши фильмов по параметрам
        film_posters = requests.get(f"{BASE_URL}/movies{invalid_parameter}")
        assert film_posters.status_code == 400, "С невалидными данными ожидается статус 400"
        assert "message" in film_posters.json()
        assert "error" in film_posters.json()
        assert "statusCode" in film_posters.json()
