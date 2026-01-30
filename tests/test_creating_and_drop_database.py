from src.creating_database import creating_database
from src.drop_database import drop_database


def test_creating_and_drop_database(capsys):
    creating_database("test")
    captured = capsys.readouterr()
    assert captured.out == "Создана база данных с именем test\n"
    creating_database("test")
    captured = capsys.readouterr()
    assert captured.out == f'ОШИБКА:  база данных "{"test"}" уже существует\n\n'
    drop_database("test")
    captured = capsys.readouterr()
    assert captured.out == "Завершение сеанса.\n База данных с именем test удалена!\n"
    drop_database("test")
    captured = capsys.readouterr()
    assert captured.out == f'ОШИБКА:  база данных "{"test"}" не существует\n\n'
