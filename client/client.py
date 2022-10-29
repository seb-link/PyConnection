from client_security import *
import socket
import os
HOST = str(input("Enter server ip address : "))  # The server's hostname or IP address
PORT = int(input("Enter Port to connect on : "))  # The port used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect() :
    try :
        s.connect((HOST, PORT))
    except:
        print("FATAL: Unable to connect to server")
        exit(1)


def send_message() :
    msg = str(input("Write message : "))
    message = encrypt(msg)
    print(message)
    del msg
    s.send(message)
    os.system("pause")

def main() :
    os.system("title client")
    connect()
    send_message()


main()
