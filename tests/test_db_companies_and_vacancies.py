import os
from unittest.mock import patch

import psycopg2
from dotenv import load_dotenv

from src.creating_database import creating_database
from src.drop_database import drop_database

load_dotenv(".env")
password = os.getenv("PASSWORD_PSQL")


def test_init_filling_in_tables(filling_in_tables):
    assert filling_in_tables._DATABASE_NAME == "companies_and_vacancies"
    assert filling_in_tables._PASSWORD == password
    assert filling_in_tables._conn_params == {
        "host": "localhost",
        "database": filling_in_tables._DATABASE_NAME,
        "user": "postgres",
        "password": filling_in_tables._PASSWORD,
    }


def test_creating_database_(filling_in_tables):
    creating_database(filling_in_tables._conn_params["database"])


def test_creating_tables(filling_in_tables):
    filling_in_tables.creating_tables()
    filling_in_tables.filling_in_table_companies()

    conn = psycopg2.connect(**filling_in_tables._conn_params)
    cur = conn.cursor()
    cur.execute("SELECT * FROM companies")
    result = cur.fetchall()
    assert len(result) == 10
    assert result[0] == (1, "Yandex")
    cur.close()
    conn.close()


@patch("requests.get")
def test_filling_in_table_vacancies(mock_get, filling_in_tables):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "items": [
            {
                "id": "128762270",
                "name": "Python разработчик (Middle+/Senior)",
                "salary": {"from": None, "to": 410000, "currency": "RUB"},
                "alternate_url": "https://hh.ru/vacancy/128762270",
                "relations": [],
                "snippet": {"requirement": "Опыт коммерческой разработки"},
            },
            {
                "id": "128762270",
                "name": "Python разработчик (Middle+/Senior)",
                "salary": None,
                "alternate_url": "https://hh.ru/vacancy/128762270",
                "relations": [],
                "snippet": {"requirement": "Опыт коммерческой разработки"},
            },
        ],
        "found": 32,
        "pages": 1,
        "page": 0,
        "per_page": 50,
        "clusters": None,
        "arguments": None,
        "fixes": None,
        "suggests": None,
        "alternate_url": "https://hh.ru/search/vacancy?area=1&enable_snippets=true&items_on_page=50&page=1&search_"
        "field=name&search_period=1&text=Python",
    }
    filling_in_tables.filling_in_table_vacancies()

    conn = psycopg2.connect(**filling_in_tables._conn_params)
    cur = conn.cursor()
    cur.execute("SELECT * FROM vacancies")
    result = cur.fetchall()
    assert len(result) == 20
    assert result[0] == (
        1,
        1,
        "Python разработчик (Middle+/Senior)",
        None,
        410000,
        "RUB",
        "https://hh.ru/vacancy/128762270",
        "Опыт коммерческой разработки",
    )
    cur.close()
    conn.close()


def test_drop_database_(filling_in_tables):
    drop_database(filling_in_tables._conn_params["database"])
