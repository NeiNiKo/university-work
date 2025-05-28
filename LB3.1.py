#Якщо що, тут поєднана реалізація двох завдань до третьої лаби, щоб усе можна було одразу перевірити і побачити що все працює гуд
import sqlite3
import hashlib

# Підключення до БД (створить файл users.db)
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Створення таблиці, якщо вона ще не існує
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    login TEXT PRIMARY KEY,
    password TEXT,
    full_name TEXT
)
''')
conn.commit()

# Функції які нам далі знадобляться

def hash_password(password):
    # Ця повертає SHA-256 хеш пароля
    return hashlib.sha256(password.encode()).hexdigest()

def add_user(login, password, full_name):
    #Ця додає нового користувача
    hashed_pw = hash_password(password)
    try:
        cursor.execute('INSERT INTO users (login, password, full_name) VALUES (?, ?, ?)',
                       (login, hashed_pw, full_name))
        conn.commit()
        print(f"Користувач {login} доданий.")
    except sqlite3.IntegrityError:
        print(f"Користувач з логіном {login} вже існує.")

def update_password(login, new_password):
    #Ця фнукція оновлює пароль користувача
    hashed_pw = hash_password(new_password)
    cursor.execute('UPDATE users SET password = ? WHERE login = ?', (hashed_pw, login))
    conn.commit()
    if cursor.rowcount == 0:
        print(f"Користувача {login} не знайдено.")
    else:
        print(f"Пароль для {login} оновлено.")

def authenticate_user(login, password):
    #Функція що перевіряє автентифікацію користувача
    hashed_pw = hash_password(password)
    cursor.execute('SELECT * FROM users WHERE login = ? AND password = ?', (login, hashed_pw))
    result = cursor.fetchone()
    if result:
        print(f"Аутентифікація успішна! Вітаємо, {result[2]}")
    else:
        print("Аутентифікація не вдалася. Неправильний логін або пароль.")

#Тестікі, або ж реалізація нашої програми
if __name__ == "__main__":
    while True:
        print("\nМеню:")
        print("1 - Додати користувача")
        print("2 - Оновити пароль")
        print("3 - Перевірити автентифікацію")
        print("4 - Вийти")

        choice = input("Ваш вибір: ")

        if choice == '1':
            login = input("Логін: ")
            password = input("Пароль: ")
            full_name = input("Повне ім'я: ")
            add_user(login, password, full_name)
        elif choice == '2':
            login = input("Логін: ")
            new_password = input("Новий пароль: ")
            update_password(login, new_password)
        elif choice == '3':
            login = input("Логін: ")
            password = input("Пароль: ")
            authenticate_user(login, password)
        elif choice == '4':
            print("Вихід.")
            break
        else:
            print("Невірний вибір.")
