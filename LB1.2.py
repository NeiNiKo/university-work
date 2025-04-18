inventory={ #Продукти на складі та їх кількість (організовано через словник)
    'яблука': 10,
    'банани': 3,
    'апельсини': 4,
    'груші': 7
}
product_name=input("Введіть назву продукту котрий хочете завезти/забрати зі складу:") #Отримаємо значення якому продукту будемо змінювати значення
change_amount=int(input("введіть зміну кількості продукту (+додати, -відняти):")) #Отримаємо значення на скільки треба змінити наявність продукту
def update_inventory(product, amount): #Створимо функцію яка перевіряє наявність продукту на складі, та змінює кількість продукту
    if product in inventory:
        inventory[product] += amount
    else:
        inventory[product] = amount
    if inventory[product] < 0:  #Якщо після змін кількість менше як 0, ставимо 0
        inventory[product] = 0
update_inventory(product_name, change_amount)
low_stock=[] #Створимо змінну, в котру запишемо продукти кількість яких менше за 5
for product_in_loop in inventory:
    if inventory[product_in_loop] < 5:
        low_stock.append(product_in_loop)
print("Мало товару на складі:", low_stock)