
try :
    import os
    import secrets
    from string import *
    import sys
except ImportError :
    print("Missing modules")
    exit(1)
try :
    from client.client_instaleur import main as clientinstall
    from serv.serv_instaleur import main as servinstall
    import pyfiglet
except ModuleNotFoundError:
    print("installing nessecary modules (this may take some time)...")
    os.system("python -m pip install cryptography")
    os.system("python -m pip install datetime")
    os.system("python -m pip uninstall pycryptodome")
    os.system("python -m pip uninstall pycrypto")
    os.system("python -m pip install pycryptodome")
    os.system("python -m pip install pyfiglet")
keysize = 4096
try :
    args1 = sys.argv[1]
    if args1 == "size=8192" :
        keysize = 8192
        print("Warning large key size may take time to generate")
    elif args1 == "size=2048" :
        keysize = 2048
    elif args1 == "size=1024" :
        keysize = 1024
except IndexError :
    pass

home = os.getcwd()
shellcode1 = f"""
import os
os.chdir(r"{home}\client")
os.startfile("client.py")
os.chdir(r"{home}\serv")
os.startfile("serv.py")

"""

name = "PyConnetion"
Author = "SebLink"
version = "0.6"

buff = pyfiglet.figlet_format(f"{name} v{version} by {Author}")
print(buff)


def installserv() :
    os.chdir("./serv")
    servinstall(keysize)
    os.chdir("..")

def installclient() :
    os.chdir("./client")
    clientinstall(keysize)
    os.chdir("..")

def installer() :
    installserv()
    installclient()
def main() :
    try :
        with open("info","r") as f :
            dat = f.read()
            del dat
    except FileNotFoundError :
        installer()
        os.chdir(home)
        hmac_key = str(input("entrer the hmac secret keys [Entrer *random* to generate a random password]: "))
        if hmac_key == "*random*" :
            try :
                len = int(input("Passw0rd lenght : "))
            except ValueError :
                exit("bye")
            alphabet = digits + ascii_letters + punctuation
            hmac_key = ''.join(secrets.choice(alphabet) for i in range(len))
            os.system("pause")
        with open("client/keyconf.txt","w") as f :
            f.write(hmac_key)
        with open("serv/keyconf.txt",'w') as f :
            f.write(hmac_key)
        with open("client/client_public_key.pem", "r") as f:
            clientkey = f.read()
        with open("serv/client_public_key.pem", "w") as f :
            f.write(clientkey)
        os.remove("client/client_public_key.pem")
        with open("serv/public_key.pem", "r") as f:
            clientkey = f.read()
        with open("client/public_key.pem", "w") as f :
            f.write(clientkey)
        os.remove("serv/public_key.pem")
        with open("main.py",'w') as f :
            f.write(shellcode1)
    with open("info","w") as f :
        f.write("installed")

if __name__ == '__main__' :
    main()