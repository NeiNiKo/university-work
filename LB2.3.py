def filter_ips(input_file_path, output_file_path, allowed_ips):
    #Словник для підрахунку дозволених IP
    ip_counts = {}

    try:
        #Читаємо вхідний файл
        with open(input_file_path, "r") as infile:
            for line in infile:
                parts = line.strip().split()
                if len(parts) == 0:
                    continue #Порожній рядок

                ip = parts[0] #IP-адреса, це перше поле в рядку

                if ip in allowed_ips:
                    ip_counts[ip] = ip_counts.get(ip, 0) + 1

    except FileNotFoundError:
        print(f"Помилка: вхідний файл '{input_file_path}' не знайдено")
        return
    except IOError:
        print(f"Помилка: не вдається прочитати файл '{input_file_path}'.'")
        return

    try:
        #Запишемо результати у вихідний файл
        with open(output_file_path, "w") as outfile:
            for ip, count in ip_counts.items():
                outfile.write(f"{ip} {count}\n")

    except IOError:
        print(f"Помилка: не вдалося записати у файл '{output_file_path}'.")
        return

    print(f"Результати записані у файл '{output_file_path}'.")

#Тестування
if __name__ == "__main__":
    #Список дозволених IP-адрес
    allowed_ips = ["192.168.127.12", "172.16.31.10", "83.149.9.216"]

    #Запускаємо функцію
    filter_ips("apache_logs.txt", "filtered_ips.txt", allowed_ips)
