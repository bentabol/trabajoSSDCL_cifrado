from config import *
from cryptography.fernet import Fernet
from getpass import getpass
import win32api
import win32file
# Seguir RBAC Pattern, crear una seguridad general que englobe todo y despues capa a capa con sus funciones y validaciones individuales
# Que solicita:
# -Interfaz CLI
# -Persistencia de datos (archivo.txt o csv)

#Comprobar integridad
import hashlib

#Tengo que configurar el pasword de forma correcta que compruebe que no es una password repetida o caracteres no aceptables
#Crear otro txt que almacene los usuarios con su rol correspondiente, su nombre de usuario y su password. 
#Para parte 2 debo controlar integridad de roles y de contactos, es decir que el programa se de cuenta que han alterado el txt de los usuarios y roles y nos lo indique
#Revisar para que los metodos sean cohesivos (Ejemplo: el metodo de leer datos hacerlo separado del de guardar e3n el fichero)

class rol():
    # Clase que engloba los roles de forma de general
    
    nameRol              = None
    añadirContact        = None
    modificarContact     = None
    eliminarContact      = None
    listarContact        = None
    añadirUser           = None
    
    def __init__(self,_nameRol,_add, _modificar,_delete,_list,_añadirUser):
        
        # Para crear un rol
        # Admin = rol(True,True,True,True,True) todo true ya que el admin cumple todas las funcionalidades
        self.nameRol           = _nameRol
        self.añadirContact     = _add
        self.modificarContact  = _modificar
        self.eliminarContact   = _delete
        self.listarContact     = _list
        self.añadirUser        = _añadirUser
    
    def __str__(self):
        def getStatus(val,index):
            if val:
                return f"{OKGREEN}[{index}]{ENDC}"
            else:
                return f"{FAIL}[{index}]{ENDC}"
        return f"""
┌─────────────────────────────────────────────┐
│\t\t{OKBLUE}O P T I O N S{ENDC}
├─────────────────────────────────────────────┤
│\t{getStatus(self.añadirContact,      0)}\tañadirContact
│\t{getStatus(self.modificarContact,   1)}\tmodificarContact
│\t{getStatus(self.eliminarContact,   2)}\teliminarContact
│\t{getStatus(self.listarContact,     3)}\tlistarContact
│\t{getStatus(self.añadirUser,         4)}\tañadirUser
│\t{OKCYAN}[5]{ENDC                   }\tClose Session
└─────────────────────────────────────────────┘
"""

class User():
    
    user = None
    password = None
    userRol = None
        
    def __init__(self,_user,_pass,_rol):
        self.user       = _user
        self.password   = _pass
        self.userRol    = _rol

    def __str__(self):
        return f'{self.user},{self.password},{(self.userRol).nameRol}\n'
    
#   Se crean los roles existentes (ESTOS VAN A SER UNICOS)

# Privilegios de ADMIN == ALL
Administrador   = rol('admin',True,True,True,True,True)
# Gestor (añadirContact, modificarContact y listarContact)
Gestor          = rol('gestor',True,True,False,True,False)
# Adistente (listarContact)
Asistente       = rol('asistente',False,False,False,True,False)

roleList=[Administrador,Gestor,Asistente]
#Los tipos de roles que existen en nuestra agenda
def getRol(strRol):
    if      'admin' in strRol:
        return Administrador
    elif    'gestor' in strRol:
        return Gestor
    elif    'asistente' in strRol:
        return Asistente

class Cerrojo():
    
    #Creamos los roles para en un futuro evaluarlos contra un rol entrante y usarlo de metodo de seguridad el Cerrojo
    userList = []
    
    def añadirUser(self,_ROL,_usuario):
        # Heredado de la clase rol el campo añadirUser (booleano)
        if _ROL.añadirUser == True:
            n = 0
            for rolesX in roleList:
                print(str(n)+" "+rolesX.nameRol)
                n +=1
            
            selectedRol = input('Ingrese el rol para el nuevo usuario')
            
            if (int(selectedRol)==0):
                _usuario.userRol = Administrador
            
            elif (int(selectedRol)==1):
                _usuario.userRol = Gestor
            
            elif (int(selectedRol)==2):
                _usuario.userRol = Asistente
            else:
                print(f"{FAIL}Ivalid rol selected{ENDC}")
            
            self.userList.append(_usuario)
            self.saveToFile()
    
    def login(self,_user,_pass):
        
        for UsuarioX in self.userList:
            if (UsuarioX.user == _user) & (UsuarioX.password == _pass):
                tmpUser = UsuarioX
                print(f"\n{OKGREEN}[OK]{ENDC}\tLogeado como {OKCYAN}{tmpUser.userRol.nameRol}{ENDC}\n")
                return tmpUser
        
        print(f"{WARNING}[WARNING]{ENDC}\tUsuario o contraseña inválidos")
        return None
    
    def comprobarHash(self):
        # Leer el ultimo HASH valido
        with open('hashU.txt','r') as f:
            HASH_last = f.readline()
            #print(PRIMER_HASH_USERS)
            
            #Comparar si el HASH para los archivos actuales coincide con el ultimo HASH

            #   Ejecutamos la funcion HASH sobre el archivo Users.txt
            with open('Users.txt',"rb") as f:
                bytes = f.read() # Leer el fichero entero como solo bytes
                readable_hash1 = hashlib.sha256(bytes).hexdigest()
                #print(readable_hash1)  --> Para mostrar la cadena hash generada
                if(readable_hash1 in HASH_last):
                    print(f"\n{OKGREEN}[OK]{ENDC}\tHASH validado correctamente para {OKCYAN}Users file{ENDC}")
                else:
                    print(f"{WARNING}[WAR]{ENDC}\tHASH invalido para fichero Users")
                f.close()
            f.close()
            
        #   Leemos el ultimo HASH guardado de Contacts
        with open('hashC.txt','r') as f:
            HASH_last = f.readline()
            #print(HASH_last)
        
            #   Ejecutamos la funcion HASH sobre el archivo
            with open('Contacts_cifrado',"rb") as f:
                bytes = f.read() # Leer el fichero entero como solo bytes
                readable_hash1 = hashlib.sha256(bytes).hexdigest()
                #print(readable_hash1) --> Para mostrar la cadena hash generada
                if(readable_hash1 in HASH_last):
                    print(f"\n{OKGREEN}[OK]{ENDC}\tHASH validado correctamente para {OKCYAN}Contacts file{ENDC}")
                else:
                    print(f"{WARNING}[WAR]{ENDC}\tHASH invalido para fichero Contacts")
                f.close()
            f.close()
            
    def __init__(self):
        self.cargarDatosFichero()
        print(f"{OKGREEN}[OK]{ENDC}\tRol de users cargados")
        
        #   Se crea un USUARIO ROOT con privilegios de admin
        root = User('admin','1234', Administrador)
        if not self.userInList(root):
            self.userList.append(root)
            self.saveToFile()
    
    def userInList(self,_user):
        for cadaUser in self.userList:
            if cadaUser.user == _user.user:
                return True
        return False
    
    def cargarDatosFichero(self):
        with open('Users.txt','r') as f:
            while True:
                line = f.readline()
                # Linea en blanco -> \n
                if ',' in line:
                    tmp = line.split(",")
                    tmp = User(tmp[0],tmp[1],getRol(tmp[2]))
                    self.userList.append(tmp)
                elif len(line)<2:
                    break
            f.close()

    def saveToFile(self):
        #llegado a este punto tenemos el Cerrojo y los usuarios con roles en la RAM -> volcar a un archivo
        with open('Users.txt','w') as f:
            for cadaUser in self.userList:
                f.write(str(cadaUser))
            f.close()

# Persona para Contacto
class Persona():
    #Datos de cada persona dentro de la agenda
    id=None
    Nombre = None
    Apellido = None
    NroTelefono = None
    
    def __init__(self, nombre, apellido, numero):
        self.Nombre=nombre
        self.Apellido=apellido
        self.NroTelefono=numero        

    def __str__(self):
        def eval(stringX):
            if len(stringX)<8:
                return '\t\t'
            else:
                return '\t'
        return f"{self.Nombre}{eval(self.Nombre)}{self.Apellido}{eval(self.Apellido)}{self.NroTelefono}"

def dialogoCrearPersona():
   nombre = input("Nombre: ")
   apellido = input("Apellido: ")
   numero = input("Numero: ")
   return Persona(nombre,apellido,numero)

#Clase agenda  
class Agenda():
    
    # Cerrojo
    cerrojo = Cerrojo()
    path = None
    Contactos = []
    
    def __init__(self,_path=None):
        if _path!=None:
            self.path = _path
    
    #Se supone que esperamos una persona (contacto)
    def añadirContact(self, _ROL):
        tmp = dialogoCrearPersona()
        result = input(f"quiere confirmar añadir a {tmp.Nombre} a la agenda yes/no: ")
        if result == "yes":
            #Capa especifica de seguridad que se encarga de validar si el rol es el correcto
            #Si el rol es valido se sincroniza la agenda si no lo es, se aborta
            if _ROL.añadirContact:
                print(f'{OKGREEN}[OK]{ENDC}\t{tmp.Nombre} added to Contacts')
                self.Contactos.append(tmp)
                self.sync()
            else:
                self.notRole()
        else:
            print(f"{FAIL}operacion abortada por el usuario{ENDC}")
    
    #Capa especifica de seguridad que se encarga de validar si el rol es el correcto
    def modificarContact(self, _ROL=None):
        print("Dialogo Modificar Persona:")
        modificado = False
        if _ROL.modificarContact:
            
            def getContacts(findContact):
                listC = []
                for cadaContact in self.Contactos:
                    if findContact in cadaContact.Nombre:
                        listC.append(cadaContact)
                return listC
            
            listaTmp = getContacts(input("Buscar contacto: "))
            
            #Imprimimos los contactos coincidentes
            for option, contacto in enumerate(listaTmp):
                print(f"Result option: [{option}]\n{contacto}")
            
            selectOption = int(input("Seleccionamos el Contacto que queremos modificar: "))
            
            if selectOption in  range(0,len(listaTmp)):
                ContactoTmp = dialogoCrearPersona()
                index = self.Contactos.index(listaTmp[selectOption])
                self.Contactos[index] = ContactoTmp
                modificado = True
            else:
                print(f"{OKGREEN}Opcion incorrecta. Abort{ENDC}")
            
            if modificado:
                print(f"{OKGREEN}Modificado{ENDC}")
                self.sync()
            else:
                print(f"{FAIL}Error en el intento de modificar Contacto{ENDC}")
                
        else:
            print(f"{FAIL}[FAIL]{ENDC}\t{_ROL.nameRol} no tiene derechos para ejecutar esa Accion")
            return False
    
    #Capa especifica de seguridad que se encarga de validar si el rol es el correcto
    def eliminarContact(self, llave=None):
        print("Dialogo Eliminar Persona:")
        nombre = input("Indique el nombre a eliminar en la agenda: ")
        eliminado = False
        
        if llave.eliminarContact:
            if ((nombre!=None)):
                cont = 0
                for cadaContacto in self.Contactos:
                    if cadaContacto.Nombre == nombre:
                        tmp = cadaContacto
                        self.Contactos.pop(cont)
                        eliminado = True
                    cont+=1
            if eliminado:
                print("Success")
                self.sync()
            else:
                print("Fail")
        else:
            print(f"{llave.nameRol} no tiene derechos para ejecutar esa Accion")
         
    #Capa especifica de seguridad que se encarga de validar si el rol es el correcto
    def listarContact(self, _ROL):
        print("Dialogo Listar Agenda: ")
        if _ROL.listarContact:
            print(HEADER_LISTAR)
            for cadaContacto in self.Contactos:
                print(cadaContacto)
        else:
            print(f"{_ROL.nameRol} no tiene derechos para ejecutar esa Accion")
    
    #Specyfic Layer
    def añadirUser(self,_ROL):
        print("Dialogo añadir Usuario:")
         #Capa especifica de seguridad que se encarga de validar si el rol es el correcto
        _user = input("usuario: ")
        _pass = getpass("password: ")
        _pass2 = getpass("Confirme:\npassword: ")
        if _pass == _pass2:
            usuario = User(_user,_pass,None)
            self.cerrojo.añadirUser(_ROL,usuario)
            self.sync()
        else:
            #capa de seguridad que solicita de nuevo la password por posibles errores
            print("Passwords no coincide")        
    
    #Specyfic Layer
    def notRole(self):
        print(f"{FAIL}[FAIL]{ENDC}\tNot a valid role")
    
    #Specyfic Layer
    #   Sincronizar Contactos
    def sync(self):
        
        with open (self.path,'w') as f:
            for x in self.Contactos:
                f.write(x.Nombre+","+x.Apellido+","+x.NroTelefono+"\n")
            
            #Se ha modificado el archivo
            f.close()
            
            #   Ejecutamos la funcion HASH una vez que hemos modificado el archivo
            #   Añadir nuevo HASH para validar la modificacion de Contactos
        
        with open ('Contacts.txt','rb') as f:
            bytes = f.read() # read entire file as bytes
            newHash = hashlib.sha256(bytes).hexdigest()
            
            with open ('hashC.txt','w') as f:
                f.write(newHash)
                f.close()
            
            
    
    def cargarDatosFichero(self, _ROL):
        if type(_ROL) == rol:
            
            listTMP=[]
            
            with open(self.path,'r') as fichero_cifrado:
                 
                    
                    try:
                        license = open('license.bin','r')
                        print(f"{OKGREEN}[OK]{ENDC}\tLicencia Localizada\n")
                        #      Se encarga de leer la licencia para asi conseguir la criptografia de forma correcta
                        licencia            = license.readline()
                        #      Usando el manejador y la key generada con la licencia
                        myKey               = bytes(licencia,encoding='utf-8')
                        myHandler           = Fernet(myKey)
                        #      Primero ciframos y guardamos el fichero cifrado y luego desciframos y hacemos lo mismo
                        texto_cifrado       = fichero_cifrado.readline()                #str
                        fichero_cifrado.close()
                        texto_bytes         = bytes(texto_cifrado,encoding='utf-8')     #bytes(str)
                        texto_descifrado    = myHandler.decrypt(texto_bytes)            #bytes
                        Contactos_descifrado=str(texto_descifrado,encoding='utf-8')     #str
                        
                        for _ in Contactos_descifrado.split('\n'):
                            tmp = _.split(',')
                            if len(tmp)>1:
                                tmp = Persona(tmp[0],tmp[1],tmp[2])
                                
                                listTMP.append(tmp)
                        
                        self.Contactos = listTMP
                        
                        print(f"{OKGREEN}[OK]{ENDC}\tContactos cargados del fichero\n")
                    
                    except Exception as e:
                        print(f"{FAIL}[FAIL]\t{e}{ENDC}") 
               
                    
                        