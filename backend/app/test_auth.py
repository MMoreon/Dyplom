import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from fastapi.testclient import TestClient
from app.main import app
from app.utils.security import get_password_hash, verify_password
from app.database import SessionLocal
from app.models.user import User

client = TestClient(app)

def test_password_hashing():
    print("\n=== Тестирование хеширования пароля ===")
    test_password = "adminpass"
    hashed = get_password_hash(test_password)
    print(f"Пароль: {test_password}")
    print(f"Хеш: {hashed}")
    print(f"Проверка (ожидается True): {verify_password(test_password, hashed)}")
    print(f"Проверка неверного пароля (ожидается False): {verify_password('wrong', hashed)}")

def test_db_user():
    print("\n=== Тестирование пользователя в БД ===")
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == "админ").first()
        if user:
            print(f"Найден пользователь: {user.username}")
            print(f"Хеш пароля в БД: {user.password_hash}")
            print(f"Проверка пароля (ожидается True): {verify_password('adminpass', user.password_hash)}")
        else:
            print("Пользователь 'админ' не найден в БД")
    finally:
        db.close()

def test_login():
    print("\n=== Тестирование входа через API ===")
    login_data = {
        "username": "админ",
        "password": "adminpass"
    }
    
    # Правильные данные
    response = client.post("/token", data=login_data)
    print(f"Статус код (ожидается 200): {response.status_code}")
    if response.status_code == 200:
        print("Успешная аутентификация!")
        print(f"Токен: {response.json()['access_token'][:50]}...")
    else:
        print(f"Ошибка: {response.text}")

    # Неправильные данные
    response = client.post("/token", data={"username": "админ", "password": "wrong"})
    print(f"Неверный пароль статус (ожидается 401): {response.status_code}")

if __name__ == "__main__":
    test_password_hashing()
    test_db_user()
    test_login()