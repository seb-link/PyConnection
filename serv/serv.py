from datetime import datetime
import os
from time import time
from serv_security import *
import socket
import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
HOST = "0.0.0.0"
PORT = int(input("[+] please entrer port to listen on : "))  # The port used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
log_open = True
with open("keyconf.txt","r") as f :
    data = f.read()
hmac_key = data
class AESCipher(object):
    def __init__(self, key): 
        self.bs = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(self,raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode()))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]

def connect() :
    try :
        s.bind((HOST, PORT))
        s.listen()
        global conn, addr
        print("[+] Listen for connection...")
        conn, addr = s.accept()
        print(f"[+] Got connection from {addr} !")
        
    except:
        print("FATAL: an error occurred")
        #print(e)
        os.system("pause")
        exit(1)

def openlog() :
    passphrase = str(input("entrer the log password : "))
    AESCipher.__init__(AESCipher, passphrase)
    with open("log.log","r") as l:
        data = l.read()
    result = AESCipher.decrypt(AESCipher, data)
    with open("log.log", "w") as l:
        l.write(result)
    global log_open
    log_open = True

def verlog() :
    passphrase = str(input("entrer the password for close the log : "))
    AESCipher.__init__(AESCipher, passphrase)
    with open("log.log","r") as l:
        data = l.read()
    result = str(AESCipher.encrypt(AESCipher, data))
    result = result.removeprefix("b'")
    result = result.removesuffix("'")
    with open("log.log", "w") as l:
        l.write(result)
    global log_open
    log_open = False

def log(message :str) :
    if log_open == False:
        openlog()
    with open("log.log","a") as l :
        l.write(f"[{datetime.today().strftime('%d-%m-%Y %H:%M')}] de : {addr} message : {message}")
        l.write("\n")
    verlog()

def get_message() :
    msg = conn.recv(1024)
    hmac_hash = conn.recv(1024)
    hmac_hash_clear  = decrypt(hmac_hash)
    hmac_hash_clear = str(hmac_hash_clear)
    hmac_hash_clear = hmac_hash_clear.removeprefix("b'")
    hmac_hash_clear = hmac_hash_clear.removesuffix("'")
    deciphe = decrypt(msg)
    message = str(deciphe)
    message = message.removeprefix("b'")
    message = message.removesuffix("'")
    verify_sha256_signature(hmac_key, message, hmac_hash_clear)
    log(message)
    print("recv message : " + message) 
    os.system("pause")

def main() :
    os.system("title serv")
    connect()
    get_message()


if __name__ == "__main__" :
    main()
