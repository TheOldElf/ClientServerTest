import socket

# Функция для отправки запроса на сервер и получения ответа
def send_request(request):
    HOST = 'localhost'
    PORT = 12345

    # Создаем сокет и подключаемся к серверу
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    # Отправляем данные на сервер
    client_socket.send(str(request).encode())

    # Получаем ответ от сервера
    response = client_socket.recv(1024)

    # Преобразуем полученные данные из байтов в словарь
    response = eval(response.decode())

    # Закрываем соединение с сервером
    client_socket.close()

    return response

while True:
    # Выводим меню с доступными операциями
    print("Выберите операцию:")
    print("1. Регистрация карты")
    print("2. Получение баланса карты")
    print("3. Обновление баланса карты")
    print("4. Выход")

    # Ждем ввода операции от пользователя
    choice = input("Введите номер операции: ")

    if choice == '1':
        # Регистрация карты
        card_number = input("Введите номер карты: ")
        balance = float(input("Введите начальный баланс карты: "))

        request = {'command': 'register', 'card_number': card_number, 'balance': balance}
        response = send_request(request)
        print(response)
    elif choice == '2':
        # Получение баланса карты
        card_number = input("Введите номер карты: ")

        request = {'command': 'get_balance', 'card_number': card_number}
        response = send_request(request)
        print(response)
    elif choice == '3':
        # Обновление баланса карты
        card_number = input("Введите номер карты: ")
        amount = float(input("Введите сумму для обновления баланса: "))

        request = {'command': 'update_balance', 'card_number': card_number, 'amount': amount}
        response = send_request(request)
        print(response)
    elif choice == '4':
        # Выход из приложения
        break
    else:
        print("Неверный выбор операции. Попробуйте еще раз.")
    
    print()  # Пустая строка для разделения вывода операций

print("Приложение завершено.")