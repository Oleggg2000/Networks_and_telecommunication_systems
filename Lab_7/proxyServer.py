import socket
import threading
import select

SOCKS_VERSION = 5  # Константа версии прокси (Socks5)


class ProxyServer:
    def __init__(self):  # Для аунтификации в проксе
        self.username = "Oleg"
        self.password = "hardpassword"

    def handle_client(self, connection):
        version, nmethods = connection.recv(2)  # В первых двух байтах читаем версию socks и методы поддерживаемых аунтификации
        methods = self.get_available_methods(nmethods, connection)  # Получаем доступный метод аунтификации

        if 2 not in set(methods):  # Если соединение без аунтификации - шлем его далеко и на долго
            connection.close()
            return
        connection.sendall(bytes([SOCKS_VERSION, 2]))  # Сообщение сервера о своем выборе аунтификации

        if not self.verify_client(connection):  #Если не прошел аунтификацию (т.е. не правильный логин/пароль), то также шлем его лесом...
            return
        version, cmd, _, address_type = connection.recv(4)  # Читаем версию (должна быть 5), код команды и тип адреса (IPv4/IPv6)

        if address_type == 1:  #Адрес версии - IPv4
            address = socket.inet_ntoa(connection.recv(4))  # Функция из 32битного пакета переводит адрес в формат строки
        elif address_type == 3:  # Доменное имя
            domain_length = connection.recv(1)[0]  # Длина домена
            address = connection.recv(domain_length)  # Домен
            address = socket.gethostbyname(address)  # Переводит доменное имя в IPv4
        port = int.from_bytes(connection.recv(2), 'big', signed=False)  # Чтение порта в порядке от старшего к младшему (big-endian)

        try:
            if cmd == 1:  # Команда 1, судя по википедии это установка TCP/IP соединения
                remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                remote.connect((address, port))
                bind_address = remote.getsockname()
                print("Присоединен {} {}".format(address, port))
            else:
                connection.close()  # Команды с binding и UDP

            addr = int.from_bytes(socket.inet_aton(bind_address[0]), 'big', signed=False)  # Адрес соединения
            port = bind_address[1]  # Порт соединения

            reply = b''.join([  # Успешный ответ клиенту содержащий:
                SOCKS_VERSION.to_bytes(1, 'big'),  # Версию Socks
                int(0).to_bytes(1, 'big'),  # Запрос предоставлен
                int(0).to_bytes(1, 'big'),  # Зарезервированный байт
                int(1).to_bytes(1, 'big'),  # IPv4 тип последующего адреса
                addr.to_bytes(4, 'big'),  # 4 байта для адреса IPv4
                port.to_bytes(2, 'big')  # Номер порта, в порядке от старшего к младшему (big-endian)
            ])
        except Exception as e:  # Ответ об ошибке клиенту
            # return connection refused error
            reply = self.generate_failed_reply(address_type, 5)
        connection.sendall(reply)

        if reply[1] == 0 and cmd == 1:  # Если это не ошибка и код команды 1 (установка TCP/IP соединения)
            self.exchange_loop(connection, remote)  # Обмен данными
        connection.close()  # Когда обмен даннымы закончен

    def exchange_loop(self, client, remote):
        while True:
            r, w, e = select.select([client, remote], [], [])  # Ждем пока клиент или прокси-сервер могут передать данные
            if client in r:  # Клиент -> Прокси
                data = client.recv(4096)
                if remote.send(data) <= 0:
                    break
            if remote in r:  # Прокси -> Клиент
                data = remote.recv(4096)
                if client.send(data) <= 0:
                    break

    def generate_failed_reply(self, address_type, error_number):
        return b''.join([  # Ответ об ошибке клиенту
            SOCKS_VERSION.to_bytes(1, 'big'),
            error_number.to_bytes(1, 'big'),
            int(0).to_bytes(1, 'big'),
            address_type.to_bytes(1, 'big'),
            int(0).to_bytes(4, 'big'),
            int(0).to_bytes(4, 'big')
        ])

    def verify_client(self, connection):
        version = ord(connection.recv(1))  # Должен вернуть 1, если запрос содержит поток
        username_len = ord(connection.recv(1))  # Длина логина
        username = connection.recv(username_len).decode('utf-8')  #Логин
        password_len = ord(connection.recv(1))  # Длина пароля
        password = connection.recv(password_len).decode('utf-8')  #Пароль

        if username == self.username and password == self.password:  # Если пароль и логин валидные
            response = bytes([version, 0])  # Успешный ответ 0
            connection.sendall(response)
            return True

        response = bytes([version, 0xFF])  # Ответ с ошибкой 0хFF
        connection.sendall(response)
        connection.close()
        return False

    def get_available_methods(self, nmethods, connection):  # Получаем доступный метод аунтификации
        methods = []
        for i in range(nmethods):
            methods.append(ord(connection.recv(1)))
        return methods

    def run(self, host, port):  # Точка входа
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host, port))
        s.listen()

        print("Socks5 запущен на {}:{}".format(host, port))

        while True:
            conn, addr = s.accept()
            print("Новый клиент {}".format(addr))
            t = threading.Thread(target=self.handle_client, args=(conn,))
            t.start()


if __name__ == "__main__":
    proxy = ProxyServer()
    proxy.run("127.0.0.1", 8000)
