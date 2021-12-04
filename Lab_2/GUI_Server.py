import ssl
import time
from tkinter import *  # It's used for GUI
from tkinter import messagebox
from base64 import b64decode, b64encode
import configparser  # It's used to store login and password for email
from socket import *
import threading

# Initialization login and password from mail.ru and gmail.com
try:
    config = configparser.ConfigParser()
    config.read("settings.ini")
    gmail_login = b64encode(config["GMAIL"]["GMAIL_LOGIN"].encode('utf-8'))
    gmail_pass = b64encode(config["GMAIL"]["GMAIL_PASSWORD"].encode('utf-8'))
except KeyError:
    print("Используйте свой логин , а затем пароль от gmail!")
    gmail_login = b64encode(input("Введите логин: ").encode('utf-8'))
    gmail_pass = b64encode(input("Введите пароль: ").encode('utf-8'))


def Receive_data(socket_):
    recv = socket_.recv(1024)
    print(recv)


""" #Using just a command line 
    msg = "   "
    while True:
        if msg[len(msg) - 1] == '.' and msg[len(msg) - 2] == '\n':
            break
        msg += "\n"
        msg += input(":::")
    msg = msg.encode("ascii")
    cSockSSL.send(msg + b"\r\n.\r\n")
    Receive_data(cSockSSL)
    cSockSSL.send("quit\r\n".encode("ascii")) # The receiver closing transmission channel
"""


# GUI
def GUI():
    def Sending_mail():
        msg = msgInput.get("1.0","end-1c")
        msg = msg.encode("ascii")
        cSockSSL.send(msg + b"\r\n.\r\n")
        Receive_data(cSockSSL)
        btn.config(state="disabled")

    WindowApp = Tk()
    WindowApp.title('GUI_Server')
    WindowApp.geometry("640x360")
    WindowApp.resizable(width=False, height=False)
    canvas = Canvas(WindowApp, height=360, width=640)
    canvas.pack()

    bgImage = PhotoImage(file = "sky.png")
    Label(WindowApp, image=bgImage).place(relwidth=1, relheight=1)

    frame = Frame(WindowApp)
    frame.place(x=180)

    title = Label(frame, text="Лабораторная работа по СиТ №2", bg="light blue", font=50)
    title.pack()

    msgInput = Text(WindowApp, bg="white", bd=5, width=75, height=5)
    msgInput.place(x=10, y=100)

    btn = Button(WindowApp, text="Отправить сообщение", bg="gray", command=Sending_mail)
    btn.place(x=485, y=200)

    WindowApp.mainloop()


# Sending_mail()  # Sending mail to the mail.ru service
forward_path = ""
gui_thread = threading.Thread(target=GUI)
gui_thread.start()


# Connecting to SMTP-server of gmail.com
mailserver = "smtp.gmail.com"
connection_socket = socket(AF_INET, SOCK_STREAM)
connection_socket.connect((mailserver, 465))
cSockSSL = ssl.wrap_socket(connection_socket) # Setting ssl(secure socket layer) connection
Receive_data(cSockSSL)

'''                                     SMTP Commands/Replies and Mail                              '''
# Authentication of person into gmail SMTP server
cSockSSL.send("ehlo host\r\n".encode("ascii"))  # The host identifies itself
Receive_data(cSockSSL)
cSockSSL.send("auth login\r\n".encode("ascii"))  # Authentication
recv = cSockSSL.recv(1024)
recv = b64decode(recv[4::])
print(recv)
cSockSSL.send(gmail_login+b"\r\n")  # Authentication login
recv = cSockSSL.recv(1024)
recv = b64decode(recv[4::])
print(recv)
cSockSSL.send(gmail_pass+b"\r\n")  # Authentication password
Receive_data(cSockSSL)

# Transaction starts
reverse_path = config["GMAIL"]["GMAIL_LOGIN"]
cSockSSL.send(f"mail from: <{reverse_path}>\r\n".encode("ascii"))  # The transaction for receiving mail starts
Receive_data(cSockSSL)
forward_path = config["MAIL"]["MAIL_LOGIN"]
cSockSSL.send(f"rcpt to: <{forward_path}>\r\n".encode("ascii"))  # It gives a forward-path identifying one recipient (possible to repeat)
Receive_data(cSockSSL)
cSockSSL.send("data\r\n".encode("ascii"))  # Command to SMTP-receiver for mail transaction, ends with new line and period
Receive_data(cSockSSL)

# Receiving mail from client
server = socket(AF_INET, SOCK_STREAM)
server.bind(('localhost', 228))
server.listen()
print("Listening")
user, address = server.accept()
print("Accepted")
receive_mail = user.recv(4636)
print(receive_mail.decode("ascii"))
messagebox.showinfo(title="Вам пришло письмо!", message=receive_mail)

# Closing SSL/TLS encrypted socket and server socket, GUI
gui_thread.join()
cSockSSL.send("quit\r\n".encode("ascii"))
Receive_data(cSockSSL)
server.close()
cSockSSL.close()
connection_socket.close()
