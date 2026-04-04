from typing import Optional

from pydantic import BaseModel, model_validator
import logging
from enums.roles import Roles
from utils.data_generator import DataGenerator

logger = logging.getLogger(__name__)

class User(BaseModel):
    email: str
    fullName: str
    password: str
    passwordRepeat: str
    roles: list[Roles]
    banned: Optional[bool] = False
    verified: Optional[bool] = False

    @model_validator(mode="before")
    def check_email_include_at(cls, values):
        """
        Проверяем, что email содержит @
        """
        if '@' not in values['email']:
            raise ValueError("!!!email должен содержать @!!!")
        if len(values['password']) < 8:
            raise ValueError("password должен быть не меньше 8 символов")
        return values


def test_user_data(test_user):
    # Convert Pydantic model to dict
    user_dict = test_user.model_dump()
    user = User(**user_dict)  # Now works
    assert isinstance(user.fullName, str)
    assert isinstance(user.password, str)
    assert user.password == user.passwordRepeat
    assert isinstance(user.roles, list)
    logger.info(user.model_dump_json())  # вместо user.json()
    logger.info(user.model_dump_json(exclude_unset=True))
    logger.info(f"{user.email=} {user.fullName=} {user.roles=}")

def test_creation_user_data(creation_user_data):
    user = User(**creation_user_data)
    assert isinstance(user.fullName, str)
    assert isinstance(user.password, str)
    assert user.password == user.passwordRepeat
    assert isinstance(user.roles, list)
    logger.info(user.model_dump_json())  # вместо user.json()
    logger.info(user.model_dump_json(exclude_unset=True))
    logger.info(f"{user.email=} {user.fullName=} {user.roles=}")

def test_registration_user_data(registration_user_data):
    registration_user_dict = registration_user_data.model_dump()
    user = User(**registration_user_dict)
    assert isinstance(user.fullName, str)
    assert isinstance(user.password, str)
    assert user.password == user.passwordRepeat
    assert isinstance(user.roles, list)
    logger.info(user.model_dump_json())
    json_data = user.model_dump_json(exclude_unset=True)
    logger.info(json_data)
    logger.info(user.model_validate_json(json_data))
    logger.info(f"{user.email=} {user.fullName=} {user.roles=}")