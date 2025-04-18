#Словник задач
tasks={
    'Підготувати звіт': 'очікує',
    'Написати код': 'в процесі',
    'Здати лабораторну': 'виконано',
    'Прочитати книгу': 'очікує',
    'Сходити за покупками': 'виконано',
}
#Функція додавання задачі
def add_task(task_name1, task_status): #Створюється дві функції з 2 параметрами - назва задачі та статус
    if task_name1 in tasks: #Перевірка чи така задача вже існує
        print(f"Задача '{task_name1}' вже існує")
    else: #Якщо не існує, додаємо нову пару назву задачі та її статус у словник
        tasks[task_name1] = task_status
        print(f"Задача '{task_name1}' додана зі статусом '{task_status}'.")
#Функція видалення задачі по назві
def remove_task(task_name1):
    if task_name1 in tasks:
        del tasks[task_name1]
        print(f"Задача '{task_name1}' була успішно видалена.")
    else:
        print(f"Задача '{task_name1}' не знайдена.")
#Функція оновлення статусу задачі
def update_status(task_name1, new_status):
    if task_name1 in tasks:
        old_status=tasks[task_name1]
        tasks[task_name1]=new_status
        print(f"Статус задачі '{task_name1}' змінено з '{old_status}' на '{new_status}'.")
    else:
        print(f"Задача '{task_name1}' не знайдена.")
#Список задач зі статусом "очікує"
waiting_tasks=[]
#Зробимо цикл перебору всіх задач та їх статусів
for task_name in tasks:
    if tasks[task_name] =="очікує": #перевіряємо статус
        waiting_tasks.append(task_name) #записуємо у список задачі з потрібним нам статусом
#Щоб перевірити виконання функцій, організуємо вивід результату їх виконання
#вивід початкового списку задач
print("Поточні задачі:")
for name, status in tasks.items():
    print(f"- {name}: {status}")

print("\nТестування функцій:")

#Виклик функцій
add_task("Написати звіт по Python", "очікує")
remove_task("Сходити за покупками")
update_status("Прочитати книгу", "в процесі")

#Вивід фінального списку задач
print("\nОновлений список задач:")
for name, status in tasks.items():
    print(f"- {name}: {status}")

#Вивід задач зі статусом "очікує"
waiting_tasks = []
for task_name in tasks:
    if tasks[task_name] == "очікує":
        waiting_tasks.append(task_name)

print("\nЗадачі, що очікують виконання:")
for task in waiting_tasks:
    print(f"- {task}")

