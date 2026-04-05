import random
import string
from faker import Faker

faker = Faker()


class DataGenerator:

    @staticmethod
    def generate_valid_film_title():
        return f"{faker.word().title()} {faker.word().title()}"

    @staticmethod
    def generate_valid_film_description():
        return faker.sentence(nb_words=10)

    @staticmethod
    def generate_random_email():
        random_string = "".join(
            random.choices(string.ascii_lowercase + string.digits, k=8)
        )
        random_char = faker.random_letter()
        return f"ke{random_char}{random_string}@gmail.com"

    @staticmethod
    def generate_random_name():
        return f"{faker.first_name()} {faker.last_name()}"

    @staticmethod
    def generate_random_password():
        """
        Генерация пароля, соответствующего требованиям:
        - Минимум 1 буква.
        - Минимум 1 цифра.
        - Допустимые символы.
        - Длина от 8 до 20 символов.
        """
        # Гарантируем наличие хотя бы одной буквы и одной цифры
        letters = random.choice(string.ascii_letters)  # Одна буква
        digits = random.choice(string.digits)  # Одна цифра

        # Дополняем пароль случайными символами из допустимого набора
        special_chars = "?@#$%^&*|:"
        all_chars = string.ascii_letters + string.digits + special_chars
        remaining_length = random.randint(6, 18)  # Остальная длина пароля
        remaining_chars = "".join(random.choices(all_chars, k=remaining_length))

        # Перемешиваем пароль для рандомизации
        password = list(letters + digits + remaining_chars)
        random.shuffle(password)

        return "".join(password)

    @staticmethod
    def generate_random_int(length: int = 10) -> int:
        """
        Генерирует случайное целое число с заданным количеством цифр.
        :param length: количество цифр в числе
        :return: случайное целое число
        """
        import random
        min_value = 10 ** (length - 1)
        max_value = (10 ** length) - 1
        return random.randint(min_value, max_value)