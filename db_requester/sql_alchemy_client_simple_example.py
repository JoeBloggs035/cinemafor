# Modul_4\Cinescope\db_requester\sql_alchemy_client_simple_example.py
from sqlalchemy import (
    create_engine,
    Column,
    String,
    Boolean,
    DateTime,
    text,
    Integer,
    Float,
    DECIMAL,
)
from sqlalchemy.orm import declarative_base, sessionmaker

# Подключение к базе данных
host = "psql.ntlg.tech"
port = 19001
database_name = "sqlfree-4"
username = "netology"
password = "NetoSQL2019"

# формируем урл для подключения к базе
connection_string = (
    f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database_name}"
)
# обьект для подключения к базе данных
engine = create_engine(connection_string)


# Modul_4\Cinescope\db_requester\sql_alchemy_client_simple_example.py
def sdl_alchemy_SQL():
    query = """
    SELECT staff_id, last_name, first_name, inn, unit_id, salary, address_id, created_date, deleted
    FROM perkov_sa.staff
    WHERE unit_id = :unit_id;
    """

    # Параметры запроса для подстановки в наш SQL запрос
    # inn = "775313475294"
    unit_id = 1

    # Выполняем запрос
    with engine.connect() as connection:  # выполняем соединение с базой данных и автоматически закрываем его по завершению выполнения
        result = connection.execute(text(query), {"unit_id": unit_id})
        for row in result:
            print(row)


# Modul_4\Cinescope\db_requester\sql_alchemy_client_simple_example.py


def sdl_alchemy_ORM():
    # Базовый класс для моделей
    Base = declarative_base()

    # Модель таблицы users
    class Staff(Base):
        __tablename__ = "staff"
        __table_args__ = {"schema": "perkov_sa"}
        staff_id = Column(Integer, primary_key=True)
        last_name = Column(String)
        first_name = Column(String)
        inn = Column(String)
        unit_id = Column(Integer)
        salary = Column(DECIMAL)
        address_id = Column(Integer)
        created_date = Column(DateTime)
        deleted = Column(Boolean)

    # Создаем сессию
    Session = sessionmaker(bind=engine)
    session = Session()

    # inn = "775313475294"
    unit_id = 1

    # Выполняем запрос
    staffs = session.query(Staff).filter(Staff.unit_id == unit_id).all()
    if not staffs:
        print("Сотрудник не найден.")
    else:
        for staff in staffs:
            print("================================================")
            print(f"Staff ID: {staff.staff_id}")
            print(f"Last name: {staff.last_name}")
            print(f"First Name: {staff.first_name}")
            print(f"Inn: {staff.inn}")
            print(f"Unit ID: {staff.unit_id}")
            print(f"Salary: {staff.salary}")
            print(f"Address ID: {staff.address_id}")
            print(f"Created Date: {staff.created_date}")
            print(f"Deleted: {staff.deleted}")


if __name__ == "__main__":
    sdl_alchemy_SQL()
    sdl_alchemy_ORM()
