import socket
import threading
import time

IsAlive = True
data = ""
Sent, Collisions = 0, 0


def receive_data(sock):
    global data
    try:
        while True:
            data = sock.recv(1024)
            if data and IsAlive is True:
                if data == b"FF" or data == b"FT" or data == b"TT":
                    continue
                else:
                    str_ = data.decode("utf-8")
                    if str(sock.getsockname()[1]) == str_[5:10:1]:
                        print(str_[10::])
            elif not data and IsAlive is True:
                continue
            elif IsAlive is False:
                break
    except KeyboardInterrupt:
        print(f"Sent messages: {Sent}\nAmount of collisions: {Collisions}")


sock = socket.socket()
sock.connect(('localhost', 8000))
print("Client connected to the bus\tInput q if you want to quit\nInput distance between server and you: ")
delay = int(input())
thread = threading.Thread(target=receive_data, args=(sock,))
thread.start()

try:
    while True:
        text = input()
        Sent += 1
        if text == "q":
            sock.send(text.encode("utf-8"))
            IsAlive = False
            print(f"Sent messages: {Sent}\nAmount of collisions: {Collisions}")
            break
        if data == b"FF":
            sock.send("FT".encode("utf-8"))
            time.sleep(delay)
            sock.send("TT".encode("utf-8"))
            time.sleep(delay)
            sock.send(text.encode("utf-8"))
            sock.send("FF".encode("utf-8"))
        elif data == b"FT":
            Collisions += 1
            print("!!! Collision detected !!!")
        elif data == b"TT":
            print("!!! Bus is busy!!!")
    thread.join()
    sock.close()
except KeyboardInterrupt:
    sock.send("q".encode("utf-8"))
    IsAlive = False
    thread.join()
    sock.close()
    print(f"Sent messages: {Sent}\nAmount of collisions: {Collisions}")
