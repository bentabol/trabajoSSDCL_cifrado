from demo import *

user,password,USER,ROL = None,None,None,None
flag = False

def login():
   print(TITLE)
   global user,password
   print(f"{HEADER}======== LOGIN ========{ENDC}")
   user        = input("login: ")
   password    = getpass("pass: ")

#[1]* Aun teniendo el path si el login no es válido, no se cargan los contactos
miAgenda = Agenda(_path='Contacts_cifrado')
login()
USER = miAgenda.cerrojo.login(user,password)

while True:
   
   #Si el login en el cerrojo devuelve un Usuario lo guardamos
   if type(USER)==User:
      ROL = USER.userRol
      
      #[1]* Con un login valido se carga completamente los contactos de la agenda
      if flag == False:
         # Añadido desde fichero
         miAgenda.cargarDatosFichero(ROL)
         miAgenda.cerrojo.comprobarHash()
         flag = True
      
      print(ROL)
      
      option = input("Selecciona opción: ")
      
      # Add Contact
      if int(option) == 0:
         miAgenda.añadirContact(_ROL=ROL)
         flag = False
            
      elif int(option) == 1:
         miAgenda.modificarContact(_ROL=ROL)
         flag = False
         
      elif int(option) == 2:
         #Capa especifica de seguridad que se encarga de validar si el rol es el correcto
         miAgenda.eliminarContact(llave=ROL)
         flag = False
         
      elif int(option) == 3:
         #Capa especifica de seguridad que se encarga de validar si el rol es el correcto
         miAgenda.listarContact(_ROL=ROL)
         
      elif int(option) == 4:
         miAgenda.añadirUser(_ROL=ROL)
         flag = False
         
      elif int(option) == 5:
         
         print(f"Sesion Concluida: {user}")
         del user, password
         del USER, ROL
         flag = False
         USER, user,password, ROL = None, None, None, None
         
   # Se devuelve None si el login falla
   else:
      login()
      USER = miAgenda.cerrojo.login(user,password)
      flag = False