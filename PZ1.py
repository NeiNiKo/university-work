import requests
import json
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# 1. Визначимо дати для отримання даних за минулий тиждень
today = datetime.today()
start_date = today - timedelta(days=7)

# 2. Перетворюємо дати в такі, щоб могли коректно потім вставити в посилання
start_str = start_date.strftime('%Y%m%d')
end_str = today.strftime('%Y%m%d')

# 3. вставляємо потрібні дати в посилання, та формуємо посилання з якого будемо брати дані
url = f"https://bank.gov.ua/NBU_Exchange/exchange_site?start={start_str}&end={end_str}&valcode=eur&json"

# 4. Робимо запрос даних, та якщо не вдасться отримати запрос, щоб вивівся код помилки (кави не бажаєте? просто так кави щось захотілось, може ви її обожнюєте?)
response = requests.get(url)
if response.status_code != 200:
    print("Помилка запиту:", response.status_code)
    exit()

# 5. Завантажуємо JSON-дані
data = json.loads(response.content)

# 6. Створюємо словник дата-курс для використання його в побудові графіку
euro_rates = {}
for item in data:
    date = item['exchangedate']  # формат дати ДД.ММ.РРРР
    rate = item['rate'] # курс євро
    euro_rates[date] = rate
    print(f"{date} - {rate} грн")

# 7. Сортуємо за датами (чогось іноді були приколи що приходили не в порядку дат, вирішив це додати на всяк на майбутнє)
dates = sorted(euro_rates.keys(), key=lambda d: datetime.strptime(d, "%d.%m.%Y"))
rates = [euro_rates[d] for d in dates]
dates_dt = [datetime.strptime(d, "%d.%m.%Y") for d in dates]

# 8. Будуємо графік
plt.plot(dates_dt, rates, marker='o', linestyle='-')
plt.title("Курс EUR за останній тиждень")
plt.xlabel("Дата")
plt.ylabel("Курс в грн")
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
