import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

class AESCipher(object):
    def __init__(self, key): 
        self.bs = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')
    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]
def main() :
    password = input("[+] entrer the log password : ")
    AESCipher.__init__(AESCipher,password)
    with open("log.log", "r") as f:
        data = f.read()
    try :
        result = AESCipher.decrypt(AESCipher, data)
    except ValueError:
        print("Oops wrong password !")
    with open("log.log", "w") as f:
        f.write(result)
    print("[+] The log are now readable !")
main()

