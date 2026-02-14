import pytest
import sqlite3
import os
from registration.registration import create_db, add_user, authenticate_user, display_users

@pytest.fixture(scope="module")
def setup_database():
    """Фикстура для настройки базы данных перед тестами и её очистки после."""
    create_db()
    yield
    try:
        os.remove('users.db')
    except PermissionError:
        pass

@pytest.fixture
def connection():
    """Фикстура для получения соединения с базой данных и его закрытия после теста."""
    conn = sqlite3.connect('users.db')
    yield conn
    conn.close()


def test_create_db(setup_database, connection):
    """Тест создания базы данных и таблицы пользователей."""
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    table_exists = cursor.fetchone()
    assert table_exists, "Таблица 'users' должна существовать в базе данных."

def test_add_new_user(setup_database, connection):
    """Тест добавления нового пользователя."""
    add_user('testuser', 'testuser@example.com', 'password123')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username='testuser';")
    user = cursor.fetchone()
    assert user, "Пользователь должен быть добавлен в базу данных."

def test_same_login(setup_database, connection):
    """Тест добавления пользователя с существующим логином."""
    result = add_user('testuser', 'testuser@example.com', 'password123')
    assert result == False

def test_authenticate(setup_database, connection):
    """Тест успешной аутентификации пользователя."""
    result1 = authenticate_user('login', '12345')
    assert result1 != None

def test_authenticate_not(setup_database, connection):
    """Тест аутентификации несуществующего пользователя."""
    result2 = authenticate_user('logi2n', '123435')
    assert result2 == False

def test_authenticate_wrong_password(setup_database, connection):
    """Тест аутентификации пользователя с неправильным паролем."""
    result3 = authenticate_user('testuser', 'password1243')
    assert result3 == False

def test_for_what_is_in(setup_database, capsys, connection):
    """Тест отображения списка пользователей."""
    display_users()
    captured = capsys.readouterr()
    assert 'login' in captured.out
    assert 'password123' not in captured.out



    