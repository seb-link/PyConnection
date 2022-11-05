from client_security import *
import socket
import os
import time
os.system("title client")
HOST = str(input("Enter server ip address : "))  # The server's hostname or IP address
if HOST == "::1" :
    HOST = "127.0.0.1"
time.sleep(0.5)
PORT = int(input("Enter Port to connect on : "))  # The port used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
with open("keyconf.txt","r") as f :
    data = f.read()
hmac_key = data

def connect() :
    try :
        s.connect((HOST, PORT))
    except:
        print("FATAL: Unable to connect to server")
        exit(1)


def send_message() :
    msg = str(input("Write message : "))
    hmac_hash = encrypt(create_sha256_signature(hmac_key,msg))
    message = encrypt(msg)
    print(f"Encrypted message : {message.hex()}")
    del msg
    s.send(message)
    s.send(hmac_hash)
    os.system("pause")

def main() :
    connect()
    time.sleep(.75)
    send_message()


main()
