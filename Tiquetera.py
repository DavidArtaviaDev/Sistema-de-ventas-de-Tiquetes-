# Es recomendable importar las clases que se usarán para type hinting (opcional pero buena práctica)
from typing import List, Optional
from Auth import Auth
from Cliente import Cliente
from Evento import Evento

class Tiquetera:
 







































































































































































































# Parte de David 

    def __init__(self):
        self.clientes = []
        self.auth = Auth(self.clientes)

    def mostraMenuPrincipal(self):
        print("DEBUG: Entrando al método mostraMenuPrincipal")  # Mensaje de depuración
        while True:
            print("\n==============================")
            print("  Bienvenido al sistema de venta de tiquetes")
            print("==============================\n")
            print("1 - Iniciar sesión (cliente/admin)")
            print("2 - Registrar cliente")
            print("3 - Salir")
            opcion = input("\nDigite la opción que desea realizar: ").strip()

            if opcion == "1":
                print("\n[Iniciar sesión seleccionado]")
                return 1
            elif opcion == "2":
                print("\n[Registrar cliente seleccionado]")
                return 2
            elif opcion == "3":
                print("\n¡Gracias por usar el sistema! Hasta luego.")
                return 3
            else:
                print("\nOpción no válida. Por favor, intente de nuevo.")
