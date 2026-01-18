from typing import Any

from src.base_parser import Parser


class HH(Parser):
    """Класс для работы с API HeadHunter"""

    _url: str = "https://api.hh.ru/vacancies"
    _vacancies: list
    _params: dict[str, Any]
    _headers: dict[str, str] = {"User-Agent": "HH-User-Agent"}

    def __init__(self) -> None:
        """Конструктор объекта класса"""
        self._params = {"page": 0, "per_page": 0, "text": "", "period": 7, "search_field": "company_name"}
        self._vacancies = []

    def connecting_to_api(self) -> list[Any]:
        """Метод подключения к API"""
        pass

    def get_vacancies(self, keyword: str) -> list:
        """Метод получения данных"""
        pass
