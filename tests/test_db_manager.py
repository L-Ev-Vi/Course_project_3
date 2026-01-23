from unittest.mock import patch


from src.creating_database import creating_database
from src.drop_database import drop_database


def test_creating_database_db(filling_in_tables):
    creating_database(filling_in_tables._conn_params["database"])


def test_init_db_manager(db):
    assert db._conn_params == {
        "host": "localhost",
        "database": db._DATABASE_NAME,
        "user": "postgres",
        "password": db._PASSWORD,
    }


def test_creating_tables_db(filling_in_tables):
    filling_in_tables.creating_tables()
    filling_in_tables.filling_in_table_companies()


@patch("requests.get")
def test_filling_in_table_vacancies_db(mock_get, filling_in_tables):
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
                "salary": {"from": 200000, "to": None, "currency": "RUB"},
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


def test_get_companies_and_vacancies_count(db, capsys):
    db.get_companies_and_vacancies_count()
    captured = capsys.readouterr()
    assert captured.out == (
        "company_name: number_vacancies\n"
        "Альфа-банк: 2\n"
        "ВЫМПЕЛКОМ: 2\n"
        "Yandex: 2\n"
        "Солар: 2\n"
        "Лига цифровой экономики: 2\n"
        "Т-Банк: 2\n"
        "Ростелеком: 2\n"
        "ВТБ: 2\n"
        "МТС ДИДЖИТАЛ: 2\n"
        "ГРИНАТОМ: 2\n"
    )


def test_get_all_vacancies(db, capsys):
    db.get_all_vacancies()
    captured = capsys.readouterr()
    assert captured.out == (
        "Yandex; Python разработчик (Middle+/Senior); от 200000; "
        "https://hh.ru/vacancy/128762270\n"
        "Yandex; Python разработчик (Middle+/Senior); до 410000; "
        "https://hh.ru/vacancy/128762270\n"
        "Ростелеком; "
        "Python разработчик (Middle+/Senior); от 200000; https://hh.ru/vacancy/128762270\n"
        "Ростелеком; "
        "Python разработчик (Middle+/Senior); до 410000; https://hh.ru/vacancy/128762270\n"
        "МТС ДИДЖИТАЛ; "
        "Python разработчик (Middle+/Senior); от 200000; https://hh.ru/vacancy/128762270\n"
        "МТС ДИДЖИТАЛ; "
        "Python разработчик (Middle+/Senior); до 410000; https://hh.ru/vacancy/128762270\n"
        "Солар; "
        "Python разработчик (Middle+/Senior); от 200000; https://hh.ru/vacancy/128762270\n"
        "Солар; "
        "Python разработчик (Middle+/Senior); до 410000; https://hh.ru/vacancy/128762270\n"
        "Альфа-банк; "
        "Python разработчик (Middle+/Senior); от 200000; https://hh.ru/vacancy/128762270\n"
        "Альфа-банк; "
        "Python разработчик (Middle+/Senior); до 410000; https://hh.ru/vacancy/128762270\n"
        "ВТБ; "
        "Python разработчик (Middle+/Senior); от 200000; https://hh.ru/vacancy/128762270\n"
        "ВТБ; "
        "Python разработчик (Middle+/Senior); до 410000; https://hh.ru/vacancy/128762270\n"
        "Т-Банк; "
        "Python разработчик (Middle+/Senior); от 200000; https://hh.ru/vacancy/128762270\n"
        "Т-Банк; "
        "Python разработчик (Middle+/Senior); до 410000; https://hh.ru/vacancy/128762270\n"
        "ГРИНАТОМ; "
        "Python разработчик (Middle+/Senior); от 200000; https://hh.ru/vacancy/128762270\n"
        "ГРИНАТОМ; "
        "Python разработчик (Middle+/Senior); до 410000; https://hh.ru/vacancy/128762270\n"
        "ВЫМПЕЛКОМ; "
        "Python разработчик (Middle+/Senior); от 200000; https://hh.ru/vacancy/128762270\n"
        "ВЫМПЕЛКОМ; "
        "Python разработчик (Middle+/Senior); до 410000; https://hh.ru/vacancy/128762270\n"
        "Лига цифровой экономики; "
        "Python разработчик (Middle+/Senior); от 200000; https://hh.ru/vacancy/128762270\n"
        "Лига цифровой экономики; "
        "Python разработчик (Middle+/Senior); до 410000; https://hh.ru/vacancy/128762270\n"
    )


def test_get_avg_salary(db, capsys):
    db.get_avg_salary()
    captured = capsys.readouterr()
    assert captured.out == "average_salary: 305000\n"


def test_get_vacancies_with_higher_salary(db, capsys):
    db.get_vacancies_with_higher_salary()
    captured = capsys.readouterr()
    assert captured.out == (
        "Yandex; Python разработчик (Middle+/Senior); до 410000; "
        "https://hh.ru/vacancy/128762270\n"
        "Ростелеком; "
        "Python разработчик (Middle+/Senior); до 410000; https://hh.ru/vacancy/128762270\n"
        "МТС ДИДЖИТАЛ; "
        "Python разработчик (Middle+/Senior); до 410000; https://hh.ru/vacancy/128762270\n"
        "Солар; "
        "Python разработчик (Middle+/Senior); до 410000; https://hh.ru/vacancy/128762270\n"
        "Альфа-банк; "
        "Python разработчик (Middle+/Senior); до 410000; https://hh.ru/vacancy/128762270\n"
        "ВТБ; "
        "Python разработчик (Middle+/Senior); до 410000; https://hh.ru/vacancy/128762270\n"
        "Т-Банк; "
        "Python разработчик (Middle+/Senior); до 410000; https://hh.ru/vacancy/128762270\n"
        "ГРИНАТОМ; "
        "Python разработчик (Middle+/Senior); до 410000; https://hh.ru/vacancy/128762270\n"
        "ВЫМПЕЛКОМ; "
        "Python разработчик (Middle+/Senior); до 410000; https://hh.ru/vacancy/128762270\n"
        "Лига цифровой экономики; "
        "Python разработчик (Middle+/Senior); до 410000; https://hh.ru/vacancy/128762270\n"
    )


def test_get_vacancies_with_keyword(db, capsys):
    db.get_vacancies_with_keyword("Python")
    captured = capsys.readouterr()
    assert captured.out == (
        "Yandex; Python разработчик (Middle+/Senior); до 410000; "
        "https://hh.ru/vacancy/128762270\n"
        "Yandex; Python разработчик (Middle+/Senior); от 200000; "
        "https://hh.ru/vacancy/128762270\n"
        "Ростелеком; "
        "Python разработчик (Middle+/Senior); до 410000; https://hh.ru/vacancy/128762270\n"
        "Ростелеком; "
        "Python разработчик (Middle+/Senior); от 200000; https://hh.ru/vacancy/128762270\n"
        "МТС ДИДЖИТАЛ; "
        "Python разработчик (Middle+/Senior); до 410000; https://hh.ru/vacancy/128762270\n"
        "МТС ДИДЖИТАЛ; "
        "Python разработчик (Middle+/Senior); от 200000; https://hh.ru/vacancy/128762270\n"
        "Солар; "
        "Python разработчик (Middle+/Senior); до 410000; https://hh.ru/vacancy/128762270\n"
        "Солар; "
        "Python разработчик (Middle+/Senior); от 200000; https://hh.ru/vacancy/128762270\n"
        "Альфа-банк; "
        "Python разработчик (Middle+/Senior); до 410000; https://hh.ru/vacancy/128762270\n"
        "Альфа-банк; "
        "Python разработчик (Middle+/Senior); от 200000; https://hh.ru/vacancy/128762270\n"
        "ВТБ; "
        "Python разработчик (Middle+/Senior); до 410000; https://hh.ru/vacancy/128762270\n"
        "ВТБ; "
        "Python разработчик (Middle+/Senior); от 200000; https://hh.ru/vacancy/128762270\n"
        "Т-Банк; "
        "Python разработчик (Middle+/Senior); до 410000; https://hh.ru/vacancy/128762270\n"
        "Т-Банк; "
        "Python разработчик (Middle+/Senior); от 200000; https://hh.ru/vacancy/128762270\n"
        "ГРИНАТОМ; "
        "Python разработчик (Middle+/Senior); до 410000; https://hh.ru/vacancy/128762270\n"
        "ГРИНАТОМ; "
        "Python разработчик (Middle+/Senior); от 200000; https://hh.ru/vacancy/128762270\n"
        "ВЫМПЕЛКОМ; "
        "Python разработчик (Middle+/Senior); до 410000; https://hh.ru/vacancy/128762270\n"
        "ВЫМПЕЛКОМ; "
        "Python разработчик (Middle+/Senior); от 200000; https://hh.ru/vacancy/128762270\n"
        "Лига цифровой экономики; "
        "Python разработчик (Middle+/Senior); до 410000; https://hh.ru/vacancy/128762270\n"
        "Лига цифровой экономики; "
        "Python разработчик (Middle+/Senior); от 200000; https://hh.ru/vacancy/128762270\n"
    )


def test_get_vacancies_with_keyword_error(db, capsys):
    db.get_vacancies_with_keyword("Java")
    captured = capsys.readouterr()
    assert captured.out == "Ничего не найдено!\n " "Попробуйте ввести запрос с ЗАГЛАВНОЙ БУКВЫ.\n"


def test_drop_database_db(filling_in_tables):
    drop_database(filling_in_tables._conn_params["database"])
