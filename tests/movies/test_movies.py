import requests

from conftest import get_film_posters
from constants import BASE_URL

class TestMovies:
    def test_movies_get_positive(self, get_film_posters):
        # Получаем афиши фильмов по параметрам
        film_posters = requests.get(f"{BASE_URL}/movies{get_film_posters}")
        assert film_posters.status_code == 200, "Ошибка при получении афиш фильмов"
        print(f"\nURL: {BASE_URL}/movies{get_film_posters}\n", film_posters.json())
        # Запись в файл
        """with open('response_film_posters.txt', 'a', encoding='utf-8') as f:
            f.write(f"\nURL: {BASE_URL}/movies{get_film_posters}\n")
            f.write(f"{film_posters.json()}\n")
            f.write("-" * 50 + "\n")
        """
        assert 'count' in film_posters.json()
        assert 'page' in film_posters.json()
        assert 'pageSize' in film_posters.json()
        assert 'pageCount' in film_posters.json()
