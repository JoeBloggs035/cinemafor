from constants import AUTH_BASE_URL
from custom_requester.custom_requester import CustomRequester


class UserAPI(CustomRequester):
    """
    Класс для работы с API пользователей.
    """

    def __init__(self, session):
        self.session = session
        super().__init__(session)

    def get_user_info(self, user_id, expected_status=200):
        """
        Получение информации о пользователе.
        :param user_id: ID пользователя.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="GET",
            base_url=AUTH_BASE_URL,
            endpoint=f"/user/{user_id}",
            expected_status=expected_status,
        )

    def get_user(self, user_locator, expected_status=200):
        return self.send_request(
            "GET",
            AUTH_BASE_URL,
            f"/user/{user_locator}",
            expected_status=expected_status,
        )

    def create_user(self, user_data, expected_status=201):
        return self.send_request(
            method="POST",
            base_url=AUTH_BASE_URL,
            endpoint="/user",
            data=user_data,
            expected_status=expected_status,
        )

    def delete_user(self, user_id, expected_status=204):
        """
        Удаление пользователя.
        :param user_id: ID пользователя.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="DELETE",
            base_url=AUTH_BASE_URL,
            endpoint=f"/user/{user_id}",
            expected_status=expected_status,
        )
