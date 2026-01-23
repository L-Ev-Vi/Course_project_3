def test_init_api_hh(hh1):
    assert hh1._url == "https://api.hh.ru/vacancies"
    assert hh1._headers == {"User-Agent": "HH-User-Agent"}
    assert hh1._params == {"page": 0, "per_page": 0, "text": "", "period": 7, "search_field": "company_name"}
    assert hh1._vacancies == []
    assert hh1.connecting_to_api() == []
    assert hh1.get_vacancies("python") == []
