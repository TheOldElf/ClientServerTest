import socket
import sqlite3

# Соединение с базой данных SQLite
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Создаем таблицу карт, если она не существует
cursor.execute('''CREATE TABLE IF NOT EXISTS cards
                  (card_number TEXT PRIMARY KEY, balance REAL)''')

# Функция для обработки запросов от клиента
def handle_request(request):
    command = request['command']
    if command == 'register':
        card_number = request['card_number']
        balance = request['balance']
        try:
            cursor.execute('INSERT INTO cards VALUES (?, ?)', (card_number, balance))
            conn.commit()
            return {'status': 'success', 'message': 'Card registered successfully.'}
        except sqlite3.IntegrityError:
            return {'status': 'error', 'message': 'Card already registered.'}
    elif command == 'get_balance':
        card_number = request['card_number']
        cursor.execute('SELECT balance FROM cards WHERE card_number = ?', (card_number,))
        result = cursor.fetchone()
        if result is not None:
            balance = result[0]
            return {'status': 'success', 'balance': balance}
        else:
            return {'status': 'error', 'message': 'Card not found.'}
    elif command == 'update_balance':
        card_number = request['card_number']
        amount = request['amount']
        cursor.execute('SELECT balance FROM cards WHERE card_number = ?', (card_number,))
        result = cursor.fetchone()
        if result is not None:
            balance = result[0]
            new_balance = balance + amount
            cursor.execute('UPDATE cards SET balance = ? WHERE card_number = ?', (new_balance, card_number))
            conn.commit()
            return {'status': 'success', 'message': 'Balance updated successfully.'}
        else:
            return {'status': 'error', 'message': 'Card not found.'}
    else:
        return {'status': 'error', 'message': 'Invalid command.'}

# Настройки сервера
HOST = 'localhost'
PORT = 12345

# Создаем сокет и связываем его с хостом и портом
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print('Server started. Listening on {}:{}'.format(HOST, PORT))

while True:
    # Ожидаем подключение клиента
    client_socket, addr = server_socket.accept()
    print('Connected by', addr)

    data = client_socket.recv(1024)
    if not data:
        break

    # Преобразуем полученные данные из байтов в словарь
    request = eval(data.decode())

    # Обрабатываем запрос и получаем ответ
    response = handle_request(request)

    # Отправляем ответ клиенту
    client_socket.send(str(response).encode())

    client_socket.close()

conn.close()
