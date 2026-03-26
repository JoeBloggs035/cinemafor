from custom_requester.custom_requester import CustomRequester
from constants import LOGIN_ENDPOINT, REGISTER_ENDPOINT, AUTH_BASE_URL


class AuthAPI(CustomRequester):
    """
      Класс для работы с аутентификацией.
      """

    def __init__(self, session):
        super().__init__(session=session)

    def register_user(self, user_data, expected_status=201):
        """
        Регистрация нового пользователя.
        :param user_data: Данные пользователя.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="POST",
            base_url=AUTH_BASE_URL,
            endpoint=REGISTER_ENDPOINT,
            data=user_data,
            expected_status=expected_status
        )

    def login_user(self, login_data, expected_status=200):
        """
        Авторизация пользователя.
        :param login_data: Данные для логина.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="POST",
            base_url=AUTH_BASE_URL,
            endpoint=LOGIN_ENDPOINT,
            data=login_data,
            expected_status=expected_status
        )

    def authenticate(self, user_creds):
        if len(user_creds) < 2:
            raise ValueError("user_creds должны содержать email и password")

        login_data = {
            "email": user_creds[0],
            "password": user_creds[1]
        }

        response = self.login_user(login_data)
        if not response.ok:
            raise Exception(f"Login не состоялся: {response.status_code} - {response.text}")

        data = response.json()
        token = data.get("accessToken")
        if not token:
            raise ValueError("токен в ответе отсутствует или он пустой")

        self._update_session_headers(self.session, authorization=f"Bearer {token}")
