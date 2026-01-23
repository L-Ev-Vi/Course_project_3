import pytest

from src.api_hh import HH
from src.db_companies_and_vacancies import CompaniesAndVacancies
from src.db_manager import DBManager
from src.filling_in_tables import FillingInTables
from src.search_by_hh import SearchBy


@pytest.fixture
def hh1():
    return HH()


@pytest.fixture
def search():
    return SearchBy()


@pytest.fixture
def company():
    return CompaniesAndVacancies()


@pytest.fixture
def db():
    return DBManager()


@pytest.fixture
def filling_in_tables():
    return FillingInTables()
