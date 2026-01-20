import psycopg2

from src.db_companies_and_vacancies import CompaniesAndVacancies


class DBManager(CompaniesAndVacancies):
    """Клас подключения к БД в PostgreSQL"""

    def get_companies_and_vacancies_count(self) -> None:
        """Метод выполняет SQL запрос к базе данных, и возвращает список всех компаний и количество вакансий у каждой
        компании."""
        result = ["company_name: number_vacancies"]
        with psycopg2.connect(**self.conn_params) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT company_name, COUNT(*) AS number_vacancies FROM companies "
                    "JOIN vacancies USING(company_id)"
                    "GROUP BY company_name ORDER BY number_vacancies DESC"
                )
                data = cur.fetchall()
                for row in data:
                    result.append(": ".join([str(x) for x in row]))
        conn.close()
        print(*result, sep="\n")

    def get_all_vacancies(self) -> None:
        """Метод выполняет SQL запрос к базе данных и возвращает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылку на вакансию."""
        result = []
        with psycopg2.connect(**self.conn_params) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT company_name, vacancy_name, salary_from, salary_to, url_vacancy FROM companies "
                    "JOIN vacancies USING(company_id)"
                )
                data = cur.fetchall()
                for row in data:
                    row = [str(x) for x in row]
                    if row[2] == "None" and row[3] == "None":
                        row[2] = "ЗП не указана"
                        del row[3]
                    elif row[2] == "None":
                        row[3] = "до " + row[3]
                        del row[2]
                    elif row[3] == "None":
                        del row[3]
                        row[2] = "от " + row[2]
                    else:
                        row[2] = "от " + row[2]
                        row[3] = "до " + row[3]
                    result.append("; ".join(row))
        conn.close()
        print(*result, sep="\n")

    def get_avg_salary(self) -> None:
        """Метод выполняет SQL запрос к базе данных и возвращает среднюю зарплату по всем вакансиям."""
        with psycopg2.connect(**self.conn_params) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT (AVG(salary_to) + AVG(salary_from)) / 2 AS salary_avg FROM vacancies "
                    "WHERE salary_from IS NOT NULL OR salary_to IS NOT NULL"
                )
                average_salary = cur.fetchall()
                result = round(average_salary[0][0])
        conn.close()
        print(f"average_salary: {result}")

    def get_vacancies_with_higher_salary(self) -> None:
        """Метод выполняет SQL запрос к базе данных и возвращает список всех вакансий,
        у которых зарплата выше средней по всем вакансиям."""
        result = []
        with psycopg2.connect(**self.conn_params) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT company_name, vacancy_name, salary_from, salary_to, url_vacancy FROM companies "
                    "JOIN vacancies USING(company_id) "
                    "WHERE salary_from > "
                    "(SELECT (AVG(salary_to) + AVG(salary_from)) / 2 FROM vacancies "
                    "WHERE salary_from IS NOT NULL OR salary_to IS NOT NULL) OR salary_to > "
                    "(SELECT (AVG(salary_to) + AVG(salary_from)) / 2 FROM vacancies "
                    "WHERE salary_from IS NOT NULL OR salary_to IS NOT NULL)"
                )
                data = cur.fetchall()
                for row in data:
                    row = [str(x) for x in row]
                    if row[2] == "None":
                        row[3] = "до " + row[3]
                        del row[2]
                    elif row[3] == "None":
                        del row[3]
                        row[2] = "от " + row[2]
                    else:
                        row[2] = "от " + row[2]
                        row[3] = "до " + row[3]
                    result.append("; ".join(row))
        conn.close()
        print(*result, sep="\n")

    def get_vacancies_with_keyword(self, keyword: str) -> None:
        """Метод принимает ключевое слово для поиска, и возвращает список всех вакансий,
        в названии которых содержатся переданные в метод слова."""
        result = []
        vacancies = []
        with psycopg2.connect(**self.conn_params) as conn:
            with conn.cursor() as cur:
                words = keyword.split()
                for word in words:
                    cur.execute(
                        f"SELECT company_name, vacancy_name, salary_from, salary_to, url_vacancy FROM companies "
                        f"JOIN vacancies USING(company_id) WHERE vacancy_name LIKE '%{word}%'"
                    )
                    data = cur.fetchall()
                    vacancies.extend(data)
                if len(vacancies) == 0:
                    print("Ничего не найдено!\n " "Попробуйте ввести запрос с ЗАГЛАВНОЙ БУКВЫ.")
                else:
                    for row in vacancies:
                        row = [str(x) for x in row]
                        if row[2] == "None" and row[3] == "None":
                            row[2] = "ЗП не указана"
                            del row[3]
                        elif row[2] == "None":
                            row[3] = "до " + row[3]
                            del row[2]
                        elif row[3] == "None":
                            del row[3]
                            row[2] = "от " + row[2]
                        else:
                            row[2] = "от " + row[2]
                            row[3] = "до " + row[3]
                        result.append("; ".join(row))
                    print(*result, sep="\n")
        conn.close()
