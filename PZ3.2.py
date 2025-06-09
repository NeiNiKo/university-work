import sqlite3
from datetime import datetime, timedelta
#Частина 4. Функції і туди сюди різні фігні
#Функція для реєстраціх нового джерела подій

def get_id(cursor, table, column, value):
    cursor.execute(f"SELECT id FROM {table} WHERE {column} = ?", (value,))
    result = cursor.fetchone()
    return result[0] if result else None

def register_event_source(name, location, source_type):
    db_connection = sqlite3.connect("security_events.db")
    sql_executor = db_connection.cursor()
    try:
        sql_executor.execute("""
            INSERT INTO EventSource (name, location, type)
            VALUES (?, ?, ?)
        """, (name, location, source_type))
        db_connection.commit()
        print(f"Усе гуд, джерело подій '{name}' успішно додано")
    except sqlite3.IntegrityError:
        print(f"Схоже дане джерело '{name}' вже існує, додавання пропущено")
    db_connection.close()

#А тепер функція для реєстрації нового типу події
def register_event_type(type_name, severity):
    db_connection = sqlite3.connect("security_events.db")
    sql_executor = db_connection.cursor()
    try:
        sql_executor.execute("""
            INSERT INTO EventTypes (type_name, severity)
            VALUES (?, ?)
        """, (type_name, severity))
        db_connection.commit()
        print(f"Усе пройшло успішно, тип події '{type_name}' успішно додане")
    except sqlite3.IntegrityError:
        print(f"Схоже даний тип події '{type_name}' вже існує, тому додавання пропущене")
    db_connection.close()

#Тепер третя функцйія,яка буде для запису нової події безпеки

def register_security_event(source_name, event_type_name, message, ip_address=None, username=None):
    db_connection = sqlite3.connect("security_events.db")
    global sql_executor #Зробимо доступним глобально всередиині цієї функції щоб в разі чого правильно працювали функціїї які будуть нижче
    sql_executor = db_connection.cursor()
    #Отримаємо id джерела у нас функція для цього була, виокристаємо її
    source_id = get_id(sql_executor,"EventSource", "name", source_name)
    if not source_id:
        print(f"Джерело '{source_name}' не знайдено")
        db_connection.close()
        return
    #А тепер отримаємо ID типу події
    event_type_id = get_id(sql_executor,"EventTypes", "type_name", event_type_name)
    if not event_type_id:
        print(f"Тип події '{event_type_name}' не було знайдено, ехх")
        db_connection.close()
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #Вставимо подію з автоматичним timestamp(DEFAULT)
    sql_executor.execute("""
        INSERT INTO SecurityEvents (timestamp, source_id, event_type_id, message, ip_address, username)
        values (?, ?, ?, ?, ?, ?)
    """, (timestamp, source_id, event_type_id, message, ip_address, username))
    db_connection.commit()
    db_connection.close()
    print("Подію успішно внесенео в базу даних")

#Поїхали реалізовувати функції запиту даних
#Перша функція Всі події "Login Failed" за отсанні 24 години
def get_login_failed_last_24h():
    db_connection = sqlite3.connect("security_events.db")
    sql_executor = db_connection.cursor()

    # Отримати id типу події "Login Failed"
    event_type_id = get_id(sql_executor,"EventTypes", "type_name", "Login Failed")
    if not event_type_id:
        print("Тип події 'Login Failed' відсутній, знач на щастя")
        return

    # Час 24 години тому
    from datetime import datetime, timedelta
    time_24h_ago = datetime.now() - timedelta(hours=24)

    sql_executor.execute("""
        SELECT timestamp, message, ip_address, username
        FROM SecurityEvents
        WHERE event_type_id = ? AND timestamp >= ?
        ORDER BY timestamp DESC
    """, (event_type_id, time_24h_ago.strftime("%Y-%m-%d %H:%M:%S")))

    results = sql_executor.fetchall()
    db_connection.close()

    print(f"\n Події 'Login Failed' за останні 24 години ({len(results)}):")
    for row in results:
        timestamp, msg, ip, user = row
        print(f"[{timestamp}] IP: {ip or '—'}, User: {user or '—'} ➜ {msg}")

#Друга функція пошуку IP адрес в яких більше 5 невдалих спроб входу за 1 годинууу
def find_brute_force_ips():
    db_connection = sqlite3.connect("security_events.db")
    sql_executor = db_connection.cursor()

    event_type_id = get_id(sql_executor,"EventTypes", "type_name", "Login Failed")
    if not event_type_id:
        print("Опана тип події 'Login Failed' не знайдено. Святкуємоо")
        return

    sql_executor.execute("""
        SELECT ip_address, COUNT(*) as fail_count
        FROM SecurityEvents
        WHERE event_type_id = ? AND timestamp >= datetime('now', '-1 hour')
              AND ip_address IS NOT NULL
        GROUP BY ip_address
        HAVING fail_count > 5
    """, (event_type_id,))

    results = sql_executor.fetchall()
    db_connection.close()

    print("\n Дууужеее підозрілі IP з >5 невдалими входами за останню годину:")
    for ip, count in results:
        print(f"IP: {ip}, Кількість спроб: {count}")
#Трееетяяя функція пошуку яка видає всі події з рівнем Critical за останій тиждень, згруповані за джерелом
def get_critical_events_by_source():
    db_connection = sqlite3.connect("security_events.db")
    sql_executor = db_connection.cursor()

    sql_executor.execute("""
        SELECT S.name, COUNT(*) as count
        FROM SecurityEvents E
        JOIN EventSource S ON E.source_id = S.id
        JOIN EventTypes T ON E.event_type_id = T.id
        WHERE T.severity = 'Critical' AND E.timestamp >= datetime('now', '-7 days')
        GROUP BY S.name
    """)

    results = sql_executor.fetchall()
    db_connection.close()

    print("\n Події рівня 'Critical' за останній тиждень (по джерелах) (багато роботи схоже буде):")
    for source_name, count in results:
        print(f"Джерело: {source_name} — {count} подій")

#Уряя остання функція шукаємо подію що містить конкретне повідомлення
def search_events_by_keyword(keyword):
    db_connection = sqlite3.connect("security_events.db")
    sql_executor = db_connection.cursor()

    sql_executor.execute("""
        SELECT timestamp, message, ip_address, username
        FROM SecurityEvents
        WHERE message LIKE ?
        ORDER BY timestamp DESC
    """, (f"%{keyword}%",))

    results = sql_executor.fetchall()
    db_connection.close()

    print(f"\nПошук подій за ключовим словом '{keyword}':")
    for row in results:
        timestamp, msg, ip, user = row
        print(f"[{timestamp}] IP: {ip or '—'}, User: {user or '—'} ➜ {msg}")


def main_menu():
    while True:
        print("\n-+-+-+-Меню безпекового моніторингу-+-+-+-")
        print("1. Зареєструвати нове джерело подій")
        print("2. Зареєструвати новий тип події")
        print("3. Зареєструвати нову подію безпеки")
        print("4. Показати 'Login Failed' за 24 години")
        print("5. Пошук IP з >5 невдалими спробами за годину")
        print("6. Критичні події за останній тиждень (по джерелах)")
        print("7. Пошук подій за ключовим словом")
        print("0. Вихід")

        choice = input("Вибери опцію яка тобі підходить: ")

        match choice:
            case "1":
                name = input("Назва джерела: ")
                location = input("IP або розташування: ")
                source_type = input("Тип джерела: ")
                register_event_source(name, location, source_type)

            case "2":
                type_name = input("Назва типу події: ")
                severity = input("Рівень серйозності (Informational/Warning/Critical): ")
                register_event_type(type_name, severity)

            case "3":
                source = input("Назва джерела: ")
                event_type = input("Тип події: ")
                msg = input("Повідомлення: ")
                ip = input("IP-адреса (можна пропустити): ") or None
                user = input("Ім'я користувача (можна пропустити): ") or None
                register_security_event(source, event_type, msg, ip, user)

            case "4":
                get_login_failed_last_24h()

            case "5":
                find_brute_force_ips()

            case "6":
                get_critical_events_by_source()

            case "7":
                keyword = input("Введіть ключове слово для пошуку: ")
                search_events_by_keyword(keyword)

            case "0":
                print("Вихід з програми. Приємних вам несподіванок")
                break

            case _:
                print(" Я хз що це за опція. Введіть число від 0 до 7.")

if __name__ == "__main__":
    main_menu()
