import json
import logging
import os

from pydantic import BaseModel
from constants import RED, GREEN, RESET


class CustomRequester:
    """
    Кастомный реквестер для стандартизации и упрощения отправки HTTP-запросов.
    """

    base_headers = {"Content-Type": "application/json", "Accept": "application/json"}

    def __init__(self, session):
        self.session = session
        self.headers = self.base_headers.copy()
        self.logger = logging.getLogger(__name__)
        # self.logger.setLevel(logging.INFO)

    def send_request(
        self,
        method,
        base_url,
        endpoint,
        data=None,
        expected_status=200,
        need_logging=True,
    ):
        url = f"{base_url}{endpoint}"

        if isinstance(data, BaseModel):
            data = json.loads(data.model_dump_json(exclude_unset=True))
        response = self.session.request(method, url, json=data, headers=self.headers)
        if need_logging:
            self.log_request_and_response(response)
        if response.status_code != expected_status:
            raise ValueError(
                f"Unexpected status code: {response.status_code}. Expected: {expected_status}"
            )
        return response

    def _update_session_headers(self, session, **kwargs):
        """
        Обновление заголовков сессии.
        :param session: Объект requests.Session, предоставленный API-классом.
        :param kwargs: Дополнительные заголовки.
        """
        # self.session = session
        self.headers.update(kwargs)  # Обновляем базовые заголовки
        session.headers.update(self.headers)  # Обновляем заголовки в текущей сессии

    def log_request_and_response(self, response):
        """
        Логгирование запросов и ответов. Настройки логгирования описаны в pytest.ini
        Преобразует вывод в curl-like (-H хэдэеры), (-d тело)

        :param response: Объект response получаемый из метода "send_request"
        """
        try:
            request = response.request
            headers = " \\\n".join(
                [f"-H '{header}: {value}'" for header, value in request.headers.items()]
            )
            full_test_name = f"pytest {os.environ.get('PYTEST_CURRENT_TEST', '').replace(' (call)', '')}"

            body = ""
            if hasattr(request, "body") and request.body is not None:
                if isinstance(request.body, bytes):
                    body = request.body.decode("utf-8")
                elif isinstance(request.body, str):
                    body = request.body
                body = f"-d '{body}' \n" if body != "{}" else ""

            self.logger.info(
                f"{GREEN}{full_test_name}{RESET}\n"
                f"curl -X {request.method} '{request.url}' \\\n"
                f"{headers} \\\n"
                f"{body}"
            )

            response_status = response.status_code
            is_success = response.ok
            response_data = response.text
            if not is_success:
                self.logger.info(
                    f"\tRESPONSE:"
                    f"\nSTATUS_CODE: {RED}{response_status}{RESET}"
                    f"\nDATA: {RED}{response_data}{RESET}"
                )
        except Exception as e:
            self.logger.info(f"\nLogging went wrong: {type(e)} - {e}")
