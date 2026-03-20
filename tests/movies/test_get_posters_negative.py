# test_get_posters_negative.py
from typing import List, Tuple

import pytest
import requests

from constants import BASE_URL, INVALID_PARAMETERS, SPECIAL_COMBINATIONS


def generate_invalid_parameters():

    test_cases = []

    for param_name, invalid_values in INVALID_PARAMETERS.items():
        for value in invalid_values:
            # Особый случай с page
            if param_name == 'page' and value == '2147483648':
                # Если page=2147483648 заменяем на page=922337203685477568, так как это валидное int64
                value = '922337203685477568'
            test_cases.append(f"?{param_name}={value}")

    # Добавляем специальные комбинации, когда minPrice >= maxPrice
    for combination in SPECIAL_COMBINATIONS:
        test_cases.append(f"?{combination}")

    return test_cases


@pytest.mark.parametrize("invalid_parameter", generate_invalid_parameters())
def test_movies_get_negative(invalid_parameter: str):

    url = f"{BASE_URL}/movies{invalid_parameter}"
    print(f"Тестируемый URL: {url}")

    response = requests.get(url, timeout=5)

    # Проверяем статус код
    assert (response.status_code == 400), f"Для параметра {invalid_parameter} ожидается статус 400, получен {response.status_code}"

    # Проверяем структуру response body
    response_json = response.json()
    assert "message" in response_json, "Ответ не содержит поле 'message'"
    assert "error" in response_json, "Ответ не содержит поле 'error'"
    assert "statusCode" in response_json, "Ответ не содержит поле 'statusCode'"
