from unittest.mock import patch


def test_init_search_by(search):
    assert search._url == "https://api.hh.ru/vacancies"
    assert search._headers == {"User-Agent": "HH-User-Agent"}
    assert search._params == {"page": 0, "per_page": 0, "text": "", "period": 7, "search_field": "company_name"}
    assert search._vacancies == []


@patch("requests.get")
def test_get_vacancies(mock_get, search):
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
    assert search.get_vacancies("python") == [
        {
            "vacancy_id": "128762270",
            "vacancy_name": "Python разработчик (Middle+/Senior)",
            "salary_from": None,
            "salary_to": 410000,
            "salary_currency": "RUB",
            "url_vacancy": "https://hh.ru/vacancy/128762270",
            "description": "Опыт коммерческой разработки",
        },
        {
            "vacancy_id": "128762270",
            "vacancy_name": "Python разработчик (Middle+/Senior)",
            "salary_from": None,
            "salary_to": None,
            "salary_currency": None,
            "url_vacancy": "https://hh.ru/vacancy/128762270",
            "description": "Опыт коммерческой разработки",
        },
    ]
    mock_get.assert_called()


def test_get_vacancies_error(search, capsys):
    search.get_vacancies(123456)
    captured = capsys.readouterr()
    assert captured.out == "Для поиска вакансий необходимо указать ключевое слово или фразу\n"
    assert search.get_vacancies(123456) == []


@patch("requests.get")
def test_connecting_to_api_error_500(mock_get, search, capsys):
    mock_get.return_value.status_code = 500
    search.get_vacancies("python")
    captured = capsys.readouterr()
    assert captured.out == "Ошибка на стороне сервера при выполнении запроса.\n"
    assert search.get_vacancies("python") == []


@patch("requests.get")
def test_connecting_to_api_error_200(mock_get, search, capsys):
    mock_get.return_value.status_code = 302
    search.get_vacancies("python")
    captured = capsys.readouterr()
    assert captured.out == "Ошибка при выполнении запроса на базовый URL.\n"
    assert search.get_vacancies("python") == []


@patch("requests.get")
def test_connecting_to_api_error_400(mock_get, search, capsys):
    mock_get.return_value.status_code = 400
    search.get_vacancies("python")
    captured = capsys.readouterr()
    assert captured.out == "Ошибка со стороны пользователя при выполнении запроса.\n"
    assert search.get_vacancies("python") == []


@patch("requests.get")
def test_get_vacancies_pages_2(mock_get, search):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "items": [
            {
                "id": "128762270",
                "name": "Python разработчик (Middle+/Senior)",
                "salary": {"from": None, "to": 410000, "currency": "RUR"},
                "alternate_url": "https://hh.ru/vacancy/128762270",
                "relations": [],
                "snippet": {"requirement": "Опыт коммерческой разработки"},
            }
        ],
        "found": 32,
        "pages": 2,
        "page": 0,
        "per_page": 50,
        "clusters": None,
        "arguments": None,
        "fixes": None,
        "suggests": None,
        "alternate_url": "https://hh.ru/search/vacancy?area=1&enable_snippets=true&items_on_page=50&page=1&search_"
        "field=name&search_period=1&text=Python",
    }
    assert search.get_vacancies("python") == [
        {
            "vacancy_id": "128762270",
            "vacancy_name": "Python разработчик (Middle+/Senior)",
            "salary_from": None,
            "salary_to": 410000,
            "salary_currency": "RUB",
            "url_vacancy": "https://hh.ru/vacancy/128762270",
            "description": "Опыт коммерческой разработки",
        },
        {
            "vacancy_id": "128762270",
            "vacancy_name": "Python разработчик (Middle+/Senior)",
            "salary_from": None,
            "salary_to": 410000,
            "salary_currency": "RUB",
            "url_vacancy": "https://hh.ru/vacancy/128762270",
            "description": "Опыт коммерческой разработки",
        },
    ]
    mock_get.assert_called()
