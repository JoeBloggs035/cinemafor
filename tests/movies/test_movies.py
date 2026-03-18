import requests

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
