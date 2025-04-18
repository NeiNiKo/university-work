#бібліотека для хешування
import hashlib
#Словник користувачів
users = {
    'ivan23': {
        'password': hashlib.md5("123456".encode()).hexdigest(),
        'name': 'Іван Петренко'
    },
    'olga_k': {
        'password': hashlib.md5("qwerty".encode()).hexdigest(),
        'name': 'Ольга Коваль'
    },
    'admin': {
        'password': hashlib.md5("adminpass".encode()).hexdigest(),
        'name': 'Адміністратор Системи'
    }
}
#Функція перевірки користувача
def authenticate_user(login, password_input):
    if login in users:
        hashed_input = hashlib.md5(password_input.encode()).hexdigest()
        if users[login]['password'] == hashed_input:
            print(f"Вітаємо, {users[login]['name']}! Успішний вхід.")
        else:
            print("Невірний пароль.")
    else:
        print("Користувача не знайдено")
#Виконання входу
user_login=input("введіть логін: ")
user_password=input("Введіть пароль :")
authenticate_user(user_login, user_password)
