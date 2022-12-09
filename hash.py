from config import *
from cryptography.fernet import Fernet
import hashlib

with open('Contacts_cifrado',"rb") as f:
    bytes = f.read() # Leer el fichero entero como solo bytes
    readable_hash1 = hashlib.sha256(bytes).hexdigest()
    #print(readable_hash1) --> Para mostrar la cadena hash generada
    print(readable_hash1)
    print(f"\n{OKGREEN}[OK]{ENDC}\tHASH validado correctamente para {OKCYAN}Contacts file{ENDC}")
    
    f.close()