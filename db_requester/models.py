# Modul_4\Cinescope\db_requester\models.py
from sqlalchemy import create_engine, Column, String, Boolean, DateTime, text, Integer
from sqlalchemy.orm import declarative_base

# Базовый класс для моделей
Base = declarative_base()

# Modul_4\Cinescope\db_requester\models.py


# Модель базы данных для пользователя
class UserDBModel(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "public"}
    id = Column(String, primary_key=True)
    email = Column(String)
    full_name = Column(String)
    password = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    verified = Column(Boolean)
    banned = Column(Boolean)
    roles = Column(String)


# Модель для таблицы accounts_transaction_template
class AccountTransactionTemplate(Base):
    __tablename__ = "accounts_transaction_template"
    __table_args__ = {"schema": "public"}
    user = Column(String, primary_key=True)
    balance = Column(Integer, nullable=False)
