import psycopg2

from src.db_companies_and_vacancies import CompaniesAndVacancies
from src.global_variables import LIST_COMPANIES
from src.search_by_hh import SearchBy


class FillingInTables(CompaniesAndVacancies):
    """Класс для создания и заполнения таблиц в базы данных в PostgreSQL"""

    def creating_tables(self) -> None:
        """Метод создания таблиц 'companies' и 'vacancies' в базе данных."""
        try:
            with psycopg2.connect(**self.conn_params) as conn:
                with conn.cursor() as cur:
                    cur.execute("CREATE TABLE companies"
                                "(company_id serial PRIMARY KEY,"
                                "company_name varchar(50) NOT NULL);"

                                "CREATE TABLE vacancies"
                                "(vacancy_id serial PRIMARY KEY,"
                                "company_id int REFERENCES companies(company_id) NOT NULL,"
                                "vacancy_name varchar(255) NOT NULL,"
                                "salary_from int,"
                                "salary_to int,"
                                "salary_currency varchar(3),"
                                "url_vacancy varchar(255),"
                                "description text)")
            conn.close()
        except psycopg2.errors.DuplicateTable as e:
            print(e)
        except Exception as e:
            print(e)

    def filling_in_table_companies(self) -> None:
        """Метод заполнения таблицы 'companies' в базе данных."""
        try:
            with psycopg2.connect(**self.conn_params) as conn:
                with conn.cursor() as cur:
                    for i, row in enumerate(LIST_COMPANIES):
                        cur.execute(f"INSERT INTO companies VALUES (%s, %s)", (i + 1, row))
            conn.close()
        except psycopg2.errors.UniqueViolation as e:
            print(e)
        except Exception as e:
            print(e)

    def filling_in_table_vacancies(self) -> None:
        """Метод заполнения таблицы 'vacancies' в базе данных."""
        try:
            with psycopg2.connect(**self.conn_params) as conn:
                with conn.cursor() as cur:
                    parameters = ("company_id, vacancy_name, salary_from, salary_to, salary_currency, "
                                  "url_vacancy, description")
                    for i, company in enumerate(LIST_COMPANIES):
                        list_vacancies = SearchBy().get_vacancies(company)
                        for row in list_vacancies:
                            cur.execute(f"INSERT INTO vacancies ({parameters}) "
                                        f"VALUES ({", ".join(["%s"] * len(row))})",
                                        (i+1, row["vacancy_name"], row["salary_from"],
                                         row["salary_to"], row["salary_currency"], row["url_vacancy"],
                                         row["description"]))
            conn.close()
        except psycopg2.errors.UniqueViolation as e:
            print(e)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    f = FillingInTables()
    f.creating_tables()
    f.filling_in_table_companies()
    f.filling_in_table_vacancies()
