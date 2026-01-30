import os

import psycopg2
from dotenv import load_dotenv

# companies_and_vacancies


def creating_database(database_name: str) -> None:
    """Функция для создания базы данных в PostgreSQL. Функция выполняет подключение к базе данных Postgre,
    и выполняет запрос на создание БД с заданным именем 'database_name'."""
    load_dotenv(".env")
    password = os.getenv("PASSWORD_PSQL")
    try:
        conn_params = {"host": "localhost", "database": "postgres", "user": "postgres", "password": password}
        conn = psycopg2.connect(**conn_params)
        cur = conn.cursor()
        conn.autocommit = True
        cur.execute(f"CREATE DATABASE {database_name}")
        cur.close()
        conn.close()
    except psycopg2.errors.DuplicateDatabase as e:
        print(e)
    except Exception as e:
        print(e)
    else:
        print(f"Создана база данных с именем {database_name}")
