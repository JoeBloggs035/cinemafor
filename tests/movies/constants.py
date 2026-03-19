from typing import List, Dict

BASE_URL = "https://api.dev-cinescope.coconutqa.ru/"
HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}

# Определяем невалидные значения для разных типов параметров
INVALID_NUMERIC_VALUES = [
    "-1",  # отрицательное число
    "2147483648",  # больше int32
    "a",
    "б",  # буквы
    "`",
    "~",
    "!",
    "@",
    "№",
    "$",
    "%",
    "^",
    "*",  # спецсимволы
    "(",
    ")",
    "_",
    "-",
    "=",
    "|",
    "/",
    "]",
    "[",
    "}",
    "{",  # спецсимволы
    '"',
    ";",
    ":",
    "1:3",
    "?",
    ".",
    ">",
    ",",
    "<",  # спецсимволы
    "ABCDEF",
    "qwerty",
    "None",
    "NULL",
    "null"  # прочие невалидные значения
    '<script>alert("XSS")</script>',  # XSS атаки
    '<img src="x" onerror="alert("XSS")">',
    "<svg onload=alert(1)>",
    'javascript:alert("XSS")',
    "2147483648-1",  # составное значение
    "M12",  # буква+цифра
    "ё",  # кириллица
]

# Невалидные значения для int64 параметров (если такие есть)
#INVALID_INT64_VALUES = INVALID_NUMERIC_VALUES

#INVALID_INT64_VALUES[1] = "922337203685477568"  # больше int64

#INVALID_PAGESIZE_VALUES = INVALID_NUMERIC_VALUES + [
#    "2147483648-1",  # составное значение
#    "M12",  # буква+цифра
#    "ё",  # кириллица
#]

# Словарь с параметрами и их невалидными значениями
INVALID_PARAMETERS: Dict[str, List[str]] = {
    "pageSize": INVALID_NUMERIC_VALUES,
    "page": INVALID_NUMERIC_VALUES,
    "minPrice": INVALID_NUMERIC_VALUES,
    "maxPrice": INVALID_NUMERIC_VALUES,
    "locations": INVALID_NUMERIC_VALUES,
    "genreId": INVALID_NUMERIC_VALUES,
    "createdAt": INVALID_NUMERIC_VALUES,
}

# Специальные комбинации параметров
SPECIAL_COMBINATIONS = [
    "minPrice=1000&maxPrice=1000",  # равные значения
    "minPrice=1000&maxPrice=999",  # min > max
]
