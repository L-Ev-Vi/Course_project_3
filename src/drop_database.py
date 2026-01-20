import os

import psycopg2
from dotenv import load_dotenv

# Код, чтобы удалить все активные подключения к БД (перед ее удалением):
"""SELECT pg_terminate_backend(pg_stat_activity.pid)
FROM pg_stat_activity
WHERE pg_stat_activity.datname = 'companies_and_vacancies' -- ← изменить на свое название БД
  AND pid <> pg_backend_pid();"""


def drop_database(database_name: str) -> None:
    """Функция для создания базы данных в PostgreSQL. Функция выполняет подключение к базе данных Postgre,
    и выполняет запрос на создание БД с заданным именем 'database_name'."""
    load_dotenv("../.env")
    password = os.getenv("PASSWORD_PSQL")
    try:
        conn_params = {"host": "localhost", "database": "postgres", "user": "postgres", "password": password}
        conn = psycopg2.connect(**conn_params)
        cur = conn.cursor()
        conn.autocommit = True
        cur.execute(f"DROP DATABASE {database_name}")
        cur.close()
        conn.close()
    except psycopg2.errors.DuplicateDatabase as e:
        print(e)
    except Exception as e:
        print(e)
    else:
        print(f"Завершение сеанса.\n" f"База данных с именем {database_name} удалена!")
