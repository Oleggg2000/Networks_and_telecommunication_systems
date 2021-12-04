import socket
import time
from threading import Thread

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 228))
server.listen()

user = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
user2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
user, address = server.accept()
print("Accepted")
user2, address2 = server.accept()
print("Accepted")


def listen_user_3(user):
    data = user.recv(1024)
    print(data.decode("utf-8"))


def start_server():
    while True:
        a = input()
        if a == "close":
            server.shutdown()
        user.send(a.encode("utf-8"))
        time.sleep(2)
        listen_user_3(user2)




#cd desktop\study\cit\lab_1\python

if __name__ == '__main__':
    start_server()
