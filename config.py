#Script creado simplemente estetico para añadir colores a las interfaces y los mensajes
HEADER      = '\033[95m'
OKBLUE      = '\033[94m'
OKCYAN      = '\033[96m'
OKGREEN     = '\033[92m'
WARNING     = '\033[93m'
FAIL        = '\033[91m'
ENDC        = '\033[0m'
BOLD        = '\033[1m'
UNDERLINE   = '\033[4m'
#Marcos esteticos para mostrar agenda
TITLE = f"""{BOLD}
┌──────────────────────────┐
│     A  G  E  N  D  A     │
└──────────────────────────┘
{ENDC}"""

HEADER_LISTAR =f"""┌─────────────────────────────────────────────┐
│{OKBLUE}Nombre\t\tApellido\tTelefono{ENDC}
└─────────────────────────────────────────────┘"""