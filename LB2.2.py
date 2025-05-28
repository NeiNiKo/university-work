import hashlib

def generate_filehashes(*file_paths):
    #Створимо словник для зберігання результатів
    file_hashes = {}

    for path in file_paths:
        try:
            #Відкриємо файл у бінарному режимі 'rb' (хоч десь інформація з книги знадобилась яку я читав)
            with open(path, 'rb') as file:
                file_content = file.read()
                # Обчислюємо SHA-256 хеш
                file_hash = hashlib.sha256(file_content).hexdigest()
                #Зберігаємо результат у словник
                file_hashes[path] = file_hash

        except FileNotFoundError:
            print(f"Помилка: файл '{path}' не знайдено")
        except IOError:
            print(f"Помилка: не вдалося прочитати файл '{path}'.")

    #Повертаємо словник з результатами
    return file_hashes

#Тестік, я б тут написав щось ще, але хз що, тому спитаю чи добре ви почуваєтесь? надіюсь що та
if __name__ == "__main__":
    #Шлях до файлу що перевіряємо
    result = generate_filehashes('apache_logs.txt', 'file_for_LB2_2.txt') #Другий файл, попросив гпт його чимось заповнити

    print("Хеші файлів (SHA-256):")
    for file_path, file_hash in result.items():
        print(f"{file_path}: {file_hash}")