#Перша частина завдання
#Бібліотека для бази даних та для отримання поточного часу
import sqlite3
from datetime import datetime, timedelta

#Підключимось до бази даних, якщо її не існує, файл автоматично буде створено
db_connection = sqlite3.connect('security_events.db')
#Змінна для виконання SQL запитів
sql_executor = db_connection.cursor()

#Таблиці з джерелами подій
sql_executor.execute("""
CREATE TABLE IF NOT EXISTS EventSource (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    location TEXT NOT NULL,
    type TEXT NOT NULL
)
""")

#Таблиця з типами подій
sql_executor.execute("""
CREATE TABLE IF NOT EXISTS EventTypes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type_name TEXT UNIQUE NOT NULL,
    severity TEXT NOT NULL
)
""")

#Таблиця з подіями безпеки
sql_executor.execute("""
CREATE TABLE IF NOT EXISTS SecurityEvents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    source_id INTEGER NOT NULL,
    event_type_id INTEGER NOT NULL,
    message TEXT NOT NULL,
    ip_address TEXT,
    username TEXT,
    FOREIGN KEY (source_id) REFERENCES EventSource(id),
    FOREIGN KEY (event_type_id) REFERENCES EventTypes(id)
)
""")

#Друга частина завдання
#Відповідно до завдання нам треба внести дані до таблиці, потім цю частину після її виконання закоментую, щоб не виконувати кожен раз при запуску програми
#Так як я в минулій частині закрив таблицю котру ми зробили, то відкрию її знову
#Створимо змінну, яка буде спписком, вона міститиме дані для таблиці EventTypes, які ми запишемо потім
event_types = [
    ("Login Success", "Informational"),
    ("Login Failed","Warning"),
    ("Port Scan Detected", "Warning"),
    ("Malware Alert", "Critical")
]
#Далі напишемо додавання події, якщо її ще не існує, ну в нашому випадку вони всі не ісмнують, але ж може наприклад база даних пошкодитись, і деякі з них є, а деяких немає
#Якщо коротко цей цикл записує типи подій в таблицю подій, щоб цикл не падав, після внесення даних
#Якщо база даних дає помилки, типу IntegrityError тобто помилка порушення обмежень цілісності
#то ми повернемо що цей тип події вже є, і продовжимо наш цикл поки усе не запишемо в таблицю в базі даних
for type_name, severity in event_types:
    try:
        sql_executor.execute("""
            INSERT INTO EventTypes (type_name, severity)
            VALUES (?, ?)
        """, (type_name, severity))
    except sqlite3.IntegrityError:
        print(f"Тип події '(type_name)' вже існує - пропущено")

#Наступним кроком нам потрібно вставити тестові записи в таблицю EventSource

event_sources = [
    ("Firewall_A", "192.168.127.12", "Firewall"),
    ("Web_Server_B", "10.0.0.90", "Web Server"),
    ("IDS_Sensor_C", "172.0.16.9", "IDS"),
    ("Router_Alpha", "192.168.100.1", "Router"),
    ("MailGateway_X", "10.0.2.1", "Mail Server")
]
#Проведемо вставку даних як раніше робили, по суті працює так само

for name, location, source_type in event_sources:
    try:
        sql_executor.execute("""
            INSERT INTO EventSource (name, location, type)
            VALUES (?, ?, ?)
        """, (name, location, source_type))
    except sqlite3.IntegrityError:
        print(f"Джерело '{name}' вже існує - пропущено")

#Тепер нам треба внести 10+ тестових значень до таблиці SecurityEvents, я попросив гпт написати події безпеки
security_events = [
    ("Firewall_A", "Login Failed", "Invalid password from 192.168.1.20", "192.168.1.20", "admin", -5),
    ("Firewall_A", "Login Failed", "Blocked login from 192.168.1.21", "192.168.1.21", "root", -4),
    ("Firewall_A", "Login Success", "Successful login", "192.168.1.10", "admin", -3),
    ("Web_Server_B", "Port Scan Detected", "Scan from 203.0.113.5", "203.0.113.5", None, -60),
    ("Web_Server_B", "Malware Alert", "Malware signature detected", "10.0.0.10", "service", -1440),
    ("IDS_Sensor_C", "Login Failed", "Login attempt from unknown", None, "guest", -2),
    ("IDS_Sensor_C", "Login Failed", "Brute force attempt detected", "172.16.3.50", None, -1),
    ("Router_Alpha", "Login Success", "Operator login successful", None, "operator", 0),
    ("MailGateway_X", "Login Failed", "Spam sender attempt", "10.0.2.12", "spammer", -3),
    ("Firewall_A", "Login Failed", "Another fail from 192.168.1.25", "192.168.1.25", "admin", -6),
]

#Також для того щоб цці дані коректно додати до бази даних і таблиці що ми створили, ми повинні розуміти ще які айді повинні їм надати,
#НАпишемо фуцнкцію котра як раз буде отримувати айді потрібні нам
#Ця функція приймає значення таблиців в котрій ми шукатимемо, стовбчика в котрому шукаємо назву, та саму назву параметра
#Як вона знайшла значення, то отримує рядок з таблиці з значеннями, а потім повертає перше зхначення ряджка, тобто айді

def get_id(cursor, table, column, value):
    cursor.execute(f"SELECT id FROM {table} WHERE {column} = ?", (value,))
    result = cursor.fetchone()
    return result[0] if result else None

#Далі нам ще треба параметр поточного часу, тобто час коли ми записали дані в таблицю події безпеки

now = datetime.now()

#Вставимо наші події, цикл такий ж самий по логіці
#Тут в цьому циклі ми ще отримуємо айді, та обчислюємо час який зараз, для запису в таблицю

for src_name, evt_name, msg, ip, user, offset in security_events:
    source_id = get_id(sql_executor,"EventSource", "name", src_name)
    event_type_id = get_id(sql_executor,"EventTypes", "type_name", evt_name)
    timestamp = (now + timedelta(minutes=offset)).strftime("%Y-%m-%d %H:%M:%S")

    if source_id and event_type_id:
        sql_executor.execute("""
            INSERT INTO SecurityEvents (timestamp, source_id, event_type_id, message, ip_address, username)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (timestamp, source_id, event_type_id, msg, ip, user))
    else:
        print(f"[!] Пропущено подію через відсутність ID: {src_name}, {evt_name}")

#Збереження змін
db_connection.commit()
db_connection.close()
