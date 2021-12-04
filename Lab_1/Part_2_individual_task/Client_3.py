import socket
import time
from threading import Thread

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 1337))
print("Connected")
client2.connect(("127.0.0.1", 228))
print("Connected")


def listen_user_2(user):
        data = user.recv(1024)
        if data != b'':
            print(data.decode("utf-8"))
            data += b"\n#hi from 3rd client"
        return data


def start():
    while True:
        data = listen_user_2(client)
        if data != b'':
            time.sleep(1)
            client2.send(data)
            data = b''
    client.close()
    client2.close()


if __name__ == '__main__':
    start()
