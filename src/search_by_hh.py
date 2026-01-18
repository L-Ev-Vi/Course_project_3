from typing import Any

import requests

from src.api_hh import HH
from src.api_request_error import ApiRequestError, ApiRequestError400, ApiRequestError500


class SearchBy(HH):
    """Класс для поиска вакансий по API HeadHunter"""

    def __connecting_to_api(self) -> list[Any]:
        """Метод подключения к API HH.ru для получения списка вакансии"""
        vacancies = []
        try:
            while True:
                response = requests.get(self._url, params=self._params, headers=self._headers)
                if response.status_code >= 500:
                    raise ApiRequestError500
                elif response.status_code >= 400:
                    raise ApiRequestError400
                elif response.status_code != 200:
                    raise ApiRequestError
                result = response.json()
                vacancies.extend(result["items"])
                if result["pages"] - 1 == self._params["page"]:
                    break
                else:
                    self._params["page"] += 1
        except ApiRequestError500 as e:
            print(e)
            return vacancies
        except ApiRequestError400 as e:
            print(e)
            return vacancies
        except ApiRequestError as e:
            print(e)
            return vacancies
        return vacancies

    def get_vacancies(self, keyword: str, per_page: int = 50) -> list:
        """Метод получения списка вакансии с сервиса HeadHunter.ru"""
        result = []
        try:
            if type(keyword) is not str:
                raise TypeError
            self._params["text"] = keyword
            self._params["per_page"] = per_page
            vacancies = self.__connecting_to_api()
            for res in vacancies:
                if res["salary"]:
                    if res["salary"]["currency"] == "RUR":
                        res["salary"]["currency"] = "RUB"
                    result.append(
                        {
                            "vacancy_id": res["id"],
                            "vacancy_name": res["name"],
                            "salary_from": res["salary"]["from"],
                            "salary_to": res["salary"]["to"],
                            "salary_currency": res["salary"]["currency"],
                            "url_vacancy": res["alternate_url"],
                            "description": res["snippet"]["requirement"],
                        }
                    )
                else:
                    result.append(
                        {
                            "vacancy_id": res["id"],
                            "vacancy_name": res["name"],
                            "salary_from": None,
                            "salary_to": None,
                            "salary_currency": None,
                            "url_vacancy": res["alternate_url"],
                            "description": res["snippet"]["requirement"]
                        }
                    )
        except TypeError:
            print("Для поиска вакансий необходимо указать ключевое слово или фразу")
            return result
        return result
