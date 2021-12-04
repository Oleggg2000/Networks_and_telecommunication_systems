import threading
from socket import *
import time
BusisBusy, Request = "F", "F"
Collisions, Sent, Receive = 0, 0, 0
clients = []
array_addr = []
threads = []


def data_listening(connection):
    global BusisBusy, Request
    try:
        while True:
            data = connection.recv(1024)
            if data:
                if data.decode("utf-8") == "q":
                    print(f"Client {connection.getpeername()} disconnected")
                    clients.remove(connection)
                    print(clients)
                    break
                elif data.decode("utf-8") == "FT":
                    BusisBusy, Request = "F", "T"
                elif data.decode("utf-8") == "TT":
                    BusisBusy, Request = "T", "T"
                elif data.decode("utf-8") == "FF":
                    BusisBusy, Request = "F", "F"
                else:
                    send_data_to_all(data, connection)
            if not data:
                continue
    except KeyboardInterrupt:
        print(clients, threads)
        for i in clients:
            i.close()
        for i in threads:
            i.join()
        print(clients, threads)
        sock.close()



def bus_status():
    while True:
        time.sleep(2)
        for k in clients:
            k.send((BusisBusy+Request).encode("utf-8"))


def send_data_to_all(data, conn):
    for i in clients:
        if i.getpeername() != conn.getpeername():
            str_ = str(conn.getpeername()[1])
            print(str_, data[0:5:1])
            i.send(str_.encode("utf-8")+data)


if __name__ == "__main__":
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(('localhost', 8000))
    print("Server started on localhost:8000")

    while True:
        try:
            sock.listen(1)
            print("Waiting for clients...")
            conn, addr = sock.accept()
            print(f"Client {addr} connected")
            clients.append(conn)
            print(clients)

            thread = threading.Thread(target=data_listening, args=(conn,))
            thread2 = threading.Thread(target=bus_status)
            thread.start()
            thread2.start()
            threads.append(thread)
            threads.append(thread2)


        except KeyboardInterrupt:
            print(clients, threads)
            for i in clients:
                i.close()
            for i in threads:
                i.join()
            print(clients, threads)
            sock.close()
