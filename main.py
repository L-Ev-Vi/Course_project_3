import time

from src.creating_database import creating_database
from src.db_manager import DBManager
from src.drop_database import drop_database
from src.filling_in_tables import FillingInTables


# При запуске скрипта, программе потребуется несколько минут что-бы заполнить таблицы компаний и вакансий
# результирующим ответом от внешнего сервиса HeadHunter.ru

def user_interface() -> None:
    """Функция для взаимодействия с пользователем"""
    creating_database("companies_and_vacancies")
    print("Пожалуйста подождите! \n"
          "Выполняется процесс получения данных!")
    tables = FillingInTables()
    tables.creating_tables()
    tables.filling_in_table_companies()
    tables.filling_in_table_vacancies()
    db_manager = DBManager()
    while True:
        action = input(
            "Выберите возможные действия\n"
            "1 — Получить список всех компаний и количество вакансий у каждой компании;\n"
            "2 — Получить список всех вакансий с указанием названия компании;\n"
            "3 — Определить среднюю зарплату по всем вакансиям;\n"
            "4 — Получить список всех вакансий, у которых зарплата выше средней;\n"
            "5 — Получить список вакансий, по ключевым словам в названии вакансии; \n"
            "6 — Выйти из программы.\n"
            "->"
        )
        if action == "1":
            db_manager.get_companies_and_vacancies_count()
            time.sleep(2)
            print()
        elif action == "2":
            db_manager.get_all_vacancies()
            time.sleep(2)
            print()
        elif action == "3":
            db_manager.get_avg_salary()
            time.sleep(2)
            print()
        elif action == "4":
            db_manager.get_vacancies_with_higher_salary()
            time.sleep(2)
            print()
        elif action == "5":
            word = input(
                "Введите ключевые слова для поиска вакансий \n"
                "->")
            while True:
                if word == "" or len(word) < 2:
                    word = input("Введите корректное слово для поиска вакансий\n"
                                 "->")
                else:
                    break
            db_manager.get_vacancies_with_keyword(word)
            time.sleep(2)
            print()
        elif action == "6":
            drop_database("companies_and_vacancies")
            break


if __name__ == '__main__':
    user_interface()
