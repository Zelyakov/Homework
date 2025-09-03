# def add(a, b):
#    """функция, которая складывает два числа"""
#    return a + b

# 1. Запись начального лог-сообщения
with open("log.txt", "w", encoding="utf-8") as file:
    file.write("Log Entry 1\n")

# 2. Чтение содержимого файла
with open("log.txt", "r", encoding="utf-8") as file:
    content = file.read()
    print("Содержимое файла после первой записи:")
    print(content)

# 3. Добавление нового лог-сообщения
with open("log.txt", "a", encoding="utf-8") as file:
    file.write("Log Entry 2\n")

# 4. Чтение содержимого файла после добавления
with open("log.txt", "r", encoding="utf-8") as file:
    content = file.read()
    print("Содержимое файла после добавления нового лог-сообщения:")
    print(content)
