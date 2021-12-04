import socket
import time
from threading import Thread



client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 228))
print("Connected")
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 1337))
server.listen()
client2, address = server.accept()
print("Accepted")


def listen_user_1(user):
        data = user.recv(1024)
        if data != b'':
            print(data.decode("utf-8"))
            data += b'\n#hi from 2nd client'
        return data


def start_client():
    while True:
        data = listen_user_1(client)
        if data != b'':
            time.sleep(1)
            client2.send(data)
            data = b''
    client.close()
    client2.close()
    server.close()


if __name__ == '__main__':
    start_client()
