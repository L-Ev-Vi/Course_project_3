import psycopg2
from src.db_companies_and_vacancies import CompaniesAndVacancies

class DBManager(CompaniesAndVacancies):
    """Клас подключения к БД в PostgreSQL"""

    def get_companies_and_vacancies_count(self) -> str:
        """Метод выполняет SQL запрос к базе данных и возвращает список всех компаний и количество вакансий у каждой
        компании. """
        pass

    def get_all_vacancies(self) -> str:
        """Метод выполняет SQL запрос к базе данных и возвращает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылку на вакансию."""
        pass

    def get_avg_salary(self) -> str:
        """Метод выполняет SQL запрос к базе данных и возвращает среднюю зарплату по всем вакансиям."""
        pass

    def get_vacancies_with_higher_salary(self) -> str:
        """Метод выполняет SQL запрос к базе данных и возвращает список всех вакансий,
        у которых зарплата выше средней по всем вакансиям."""
        pass

    def get_vacancies_with_keyword(self) -> str:
        """Метод принимает ключевое слово для поиска, и возвращает список всех вакансий,
        в названии которых содержатся переданные в метод слова."""
        pass
