from Ticket import Ticket
from GestorTicket import GestorTicket
from Tiquetera import Tiquetera

def menu():
    tiquetera = Tiquetera()

    tiquetera.cargarDatos()
    
    tiquetera.mostraMenuPrincipal()




if __name__ == "__main__":
    menu()
