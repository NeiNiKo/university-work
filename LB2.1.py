def analyze_log_file(log_file_path):
    #Створимо порожній словник для підрахунку кодів
    status_counts={}

    try:
        #Відкриємо файл для читання
        with open(log_file_path, 'r') as file:
            for line in file:
                #Розб'ємо рядок на частини (пробілами)
                parts = line.strip().split()

                if len(parts) < 0:
                    #Якщо рядок ну якось щось дуже короткий, нафіг його посилаємо
                    continue

                #В Apache-логах код відповіді на 9-му місці (в інеті знайшов цю інфу)
                status_code = parts[8]

                #Підрахуємо кількість входжень кожного коду
                if status_code.isdigit():
                    status_counts[status_code] = status_counts.get(status_code, 0) + 1

    except FileNotFoundError:
        print(f"Помилка: файл '{log_file_path}' не знайдено, не щастить(.")
    except IOError:
        print(f"Помилка: не вдалося прочитати файл '{log_file_path}'.")

    #Поветаємо словник з результатами
    return status_counts

#Проведемо тест а ще музична пауза
#Carry on my wayward son
#There`ll be peace when you are done
#Lay your weary head to rest
#Don`t you cry no more
if __name__ == "__main__":
    log_path = "apache_logs.txt"
    result = analyze_log_file(log_path)
    print("Результати аналізу лог-файлу:")
    for code, count in result.items():
        print(f"Код {code}: {count} разів")