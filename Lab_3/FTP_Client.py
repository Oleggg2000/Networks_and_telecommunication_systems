from socket import *
from threading import Thread
import ssl
stop = False

def Receive_commands(socket_):
    socket_.settimeout(2)
    while True:
        try:
            recv = socket_.recv(1024)
            if recv == b'':
                break;
            print(recv)
        except OSError:
            break;

def Receive_data(socket_):
    recv = b""
    socket_.send("TYPE I\r\n".encode("ascii"))
    f = open("WS_FTP.LOG", "wb")
    while True:
        recv = socket_.recv(1024)
        if recv == b'':
            break
        f.write(recv)
    f.close()

def Parser_Addr(socket_):
    recv = socket_.recv(1024)
    print(recv)
    recv = recv[27:-3:].decode("utf-8")
    address = recv.split(",")
    id = ""
    for i in range(4):
        id += address[i]
        if i != 3:
            id += "."
    port = int(address[4])*256 + int(address[5])

    return (id, port)

client_active = socket(AF_INET, SOCK_STREAM)
client_passive = socket(AF_INET, SOCK_STREAM)
listening_thread = Thread(target=Receive_commands, args=(client_active,))
listening_thread2 = Thread(target=Receive_commands, args=(client_active,))
data_thread = Thread(target=Receive_data, args=(client_passive,))

client_active.connect(("home.dimonius.ru", 21))
listening_thread.start()

client_active.send("USER anonymous\r\n".encode("ascii"))
client_active.send("PASS saga6021@gmail.com\r\n".encode("ascii"))
listening_thread.join()
client_active.send("PASV\r\n".encode("ascii"))

pasv_addr = Parser_Addr(client_active)
listening_thread2.start()
client_passive.connect(pasv_addr)
#client_active.send("HELP\r\n".encode("ascii"))
client_active.send("RETR /ForUpload/Inflatables/WS_FTP.LOG\r\n".encode("ascii"))
data_thread.start()

client_active.send("QUIT\r\n".encode("ascii"))
data_thread.join()
listening_thread2.join()
client_active.close()
client_passive.close()
