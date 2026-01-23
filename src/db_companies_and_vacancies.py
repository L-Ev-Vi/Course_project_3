import os

from dotenv import load_dotenv


class CompaniesAndVacancies:
    """Базовый класс подключения к БД companies_and_vacancies в PostgreSQL"""

    # имя базы данных, в которой будут создаваться и заполнится таблицы
    _DATABASE_NAME: str = "companies_and_vacancies"
    # пароль для доступа к БД PostgreSQL
    load_dotenv(".env")
    _PASSWORD: str | None = os.getenv("PASSWORD_PSQL")

    def __init__(self) -> None:
        """Метод инициализации объекта класса"""
        self._conn_params = {
            "host": "localhost",
            "database": CompaniesAndVacancies._DATABASE_NAME,
            "user": "postgres",
            "password": CompaniesAndVacancies._PASSWORD,
        }
