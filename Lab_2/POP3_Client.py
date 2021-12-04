import configparser
import ssl
from socket import *

try:
    config = configparser.ConfigParser()
    config.read("settings.ini")
    mail_login = config["MAIL"]["MAIL_LOGIN"]
    mail_pass = config["MAIL"]["MAIL_PASSWORD"]
except KeyError:
    print("Используйте свой логин , а затем пароль от mail!")
    mail_login = input("Введите логин: ").encode('utf-8')
    mail_pass = input("Введите пароль: ").encode('utf-8')


def Receive_data(socket_):
    recv = socket_.recv(1024)
    print(recv)


# Connecting to POP-server of gmail.com
mailserver = "pop.mail.ru"
connection_socket = socket(AF_INET, SOCK_STREAM)
connection_socket.connect((mailserver, 995))
cSockSSL = ssl.wrap_socket(connection_socket)
Receive_data(cSockSSL)

# Connecting to a message storage (Step 1, Authorisation)
cSockSSL.send(f"user {mail_login}\r\n".encode("ascii"))
Receive_data(cSockSSL)
cSockSSL.send(f"pass {mail_pass}\r\n".encode("ascii"))
Receive_data(cSockSSL)

# The TRANSACTION State (Step 2, Transaction)
cSockSSL.send("stat\r\n".encode("ascii"))
Receive_data(cSockSSL)
'''cSockSSL.send("top 1606 10\r\n".encode("ascii"))
Receive_data(cSockSSL)
Receive_data(cSockSSL)'''
cSockSSL.send("list 1609\r\n".encode("ascii"))
Receive_data(cSockSSL)
cSockSSL.send("retr 1609\r\n".encode("ascii"))
Receive_data(cSockSSL)
recv = cSockSSL.recv(1024)

size=len(recv)
res2= recv
print(recv.decode("utf-8"))
while recv.decode("utf-8").find("\n.") == -1:
    recv = cSockSSL.recv(1024)
    res2=res2+recv
    size=len(recv)
print(recv.decode("utf-8"))

# Sending mail to GUI_Server
user = socket(AF_INET, SOCK_STREAM)
user.connect(('localhost', 228))
print("Connected")
user.send(recv)

# The UPDATE State
cSockSSL.send("quit\r\n".encode("ascii"))
user.close()
cSockSSL.close()
connection_socket.close()
