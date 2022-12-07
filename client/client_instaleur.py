from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def securing(key_size : int):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
    )

    with open('client_private_key.pem', 'wb') as f:
        f.write(pem)

    pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    with open('client_public_key.pem', 'wb') as f:
        f.write(pem)
    
    
def main(key_size : int) :
    with open("keyconf.txt","w") as f :
        f.close()
    securing(key_size)

if __name__ == "__main__" :
    main()