import os

from dotenv import load_dotenv


class CompaniesAndVacancies:
    """Базовый класс подключения к БД companies_and_vacancies в PostgreSQL"""

    # имя базы данных, в которой будут создаваться и заполнится таблицы
    DATABASE_NAME: str = "companies_and_vacancies"

    def __init__(self) -> None:
        """Метод инициализации объекта класса"""
        load_dotenv(".env")
        password = os.getenv("PASSWORD_PSQL")

        self.conn_params = {
            "host": "localhost",
            "database": self.DATABASE_NAME,
            "user": "postgres",
            "password": password,
        }
