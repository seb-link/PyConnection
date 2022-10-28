import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

class AESCipher(object):
    def __init__(self, key): 
        self.bs = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(self,raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode()))
    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)
        
def main() :
    password = input("[+] entrer the password to close log : ")
    AESCipher.__init__(AESCipher,password)
    with open("log.log", "r") as f:
        data = f.read()
    try :
        result = str(AESCipher.encrypt(AESCipher, data))
        result = result.removesuffix("'")
        result = result.removeprefix("b'")
    except ValueError:
        print("Invalid key")
    with open("log.log", "w") as f:
        f.write(result)
    print("[+] The log are now lock !")

if __name__ == '__main__' :
    main()
