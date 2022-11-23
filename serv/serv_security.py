import os
from Crypto.Hash import HMAC, SHA256
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
global public_key
global private_key
global pem
def get_private_key():
    with open("private_key.pem", "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )
    return private_key
def get_public_key():
    with open("client_public_key.pem", "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )
    return public_key
def encrypt(what) :
    what = str(what)
    message = bytes(what.encode())
    public_key = get_public_key()
    encrypted = public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted

def decrypt(encrypted) :
    private_key = get_private_key()
    original_message = private_key.decrypt(
        encrypted,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return original_message

    
def verify_sha256_signature(key : str, msg :str, hash):
    msg = bytes(msg.encode())
    key = bytes(key.encode())
    h = HMAC.new(key, digestmod=SHA256)
    h.update(msg)
    try:
        h.hexverify(hash)
        print("The message is authentic")
    except ValueError:
        print("The message or the key is wrong")
        os.system("pause")
        exit()