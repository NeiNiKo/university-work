import hashlib
from datetime import datetime

#Створюємо базовий клас User
class User:
    def __init__(self,username,password):
        self.username = username # ім'я користувача
        self.password_hash = self.hash_password(password) #будемо хешувати пароль, а функція для того щоб потім могли змінювати варіант хешування
        self.is_active = True # Задаємо значення чи активний користувач

    def hash_password(self, password):
        #Тут можемо потім поміняти варіант хешування, якщо буде потреба
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password):
        #Перевірка співпадіння введеного пароля з збереженим хешем
        return self.password_hash == hashlib.sha256(password.encode()).hexdigest()

#Далі підклас Administrator
class Administrator(User):
    def __init__(self,username,password):
        super().__init__(username,password) #Викликаємо ініціалізацію батьківського класу
        self.permissions = [] #Список дозволів адміністратора (типу manager_users, view_reports)

    def add_permission(self,permission):
        #Функція для додавання дозволів адміністратору
        self.permissions.append(permission)

#Підклас RegularUser (типу активні студенти)
class RegularUser(User):
    def __init__(self,username,password):
        super().__init__(username,password)  #Робимо ініціалізацію як базового User
        self.last_login = None #Зберігаємо коли останній раз входив в систему

    def update_last_login(self):
        #Якщо користувач успішно увійшов, оновлюємо час коли він останній раз увійшов в систему
        self.last_login = datetime.now()

#Підклас GuestUser (типу студенти які випадково зайшли не на ту пару)
class GuestUser(User):
    def __init__(self,username):
        #Для гостя використовуємо фіксований пароль "guest"
        super().__init__(username, password="guest")
        self.is_active = False #Гостьовий акаунт неактивний за замовчуванням (логічно думаю)

#Клас AccessControl (контроль доступу)
class AccessControl:
    def __init__(self):
        #Словник користувачів: ключ -username, значення - об'єкт User
        self.users = {}

    def add_user(self,user):
        #Функція додавання нового користувача до системи
        if user.username in self.users:
            print(f"Користувач {user.username} вже існує.")
        else:
            self.users[user.username] = user
            print(f"Користувач {user.username} доданий.")

    def authenticate_user(self, username, password):
        #Перевірочка легіт чи ні користувач вводить пароль
        user = self.users.get(username)
        if user and user.verify_password(password):
            print (f"Аутентифікація успішна для користувача {username}")
            #Якщо це звичайний користувач то оновлюємо останню дату входу
            if isinstance(user, RegularUser):
                user.update_last_login()
            return user # Повертаємо об'єкт користувача
        else:
            print(f"Футентифікація не вдалася для користувача {username}")
            return None # Ну якщо не вдалося, повернемо None, шо поробиш

#Найцікавіше, тестування програми
if __name__ == "__main__":
    #Створимо об'єкт контролю доступу
    ac = AccessControl()

    #Створимо різних користувачів
    admin = Administrator("admin","admin123")
    user = RegularUser("Bruce_wayne","iambatman")
    guest = GuestUser("guest_user")

    #Додамо цих користувачів до системи
    ac.add_user(admin)
    ac.add_user(user)
    ac.add_user(guest)

    #Перевіримо аутентифікацію
    ac.authenticate_user("admin","admin123")            #Правильний пароль
    ac.authenticate_user("Bruce_wayne","iamnotbatman")  #Брюс вейн забув пароль, і він не правильний
    ac.authenticate_user("guest_user","guest")          #Гостьовий доступ