from client.client_instaleur import main as clientinstall
from serv.serv_instaleur import main as servinstall
import pip
import os
home = os.getcwd()
requrements = ["cryptography","pycryptodome","datetime"]
shellcode1 = f"""
#!/usr/bin/python3
import os

os.chdir(r"{home}\client")
os.startfile("client.py")
os.chdir(r"{home}\serv")
os.startfile("serv.py")

"""
def installserv() :
    os.chdir("./serv")
    servinstall()
    os.chdir("..")

def installclient() :
    os.chdir("./client")
    clientinstall()
    os.chdir("..")

def installer() :
    installserv()
    installclient()
def main() :
    for n in requrements :
        if os.system(f"pip install {n}") :
            if n == "cryptography" :
                os.system("pip uninstall pycrypto")
                os.system("pip uninstall pycryptodome")
                if os.system(f"pip install {n}") :
                    print(f"Erreur pendant l'installation de {n} Stopage...")
                    return 1
            print(f"Erreur pendant l'installation de {n} Stopage...")
            return 1
    try :
        with open("info","r") as f :
            dat = f.read()
            del dat
    except FileNotFoundError :
        installer()
        os.chdir(home)
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