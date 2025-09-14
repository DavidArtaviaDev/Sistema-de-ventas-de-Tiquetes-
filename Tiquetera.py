# Es recomendable importar las clases que se usarán para type hinting (opcional pero buena práctica)
from typing import List, Optional
from Auth import Auth
from CSVManager import CSVManager
from Cliente import Cliente
from Evento import Evento
from GestorTicket import GestorTicket

class Tiquetera:

    # Parte de David

    def __init__(self):
        self.clientes = []
        self.eventos = []
        self.tickets = []

        self.cliente_actual = None  # Cliente autenticado actualmente el que esta utilizando la aplicacion en momento
        self.auth = None    # Objeto Auth para manejar autenticaciones se carga en la funcion cargarDatos



    def mostraMenuPrincipal(self):
   
        while True:
            print("\n==============================")
            print("  Bienvenido al sistema de venta de tiquetes")
            print("==============================\n")
            print("1 - Iniciar sesión (cliente/admin)")
            print("2 - Registrar cliente")
            print("3 - Salir")
            opcion = input("\nDigite la opción que desea realizar: ").strip()

            if opcion == "1":
                self.inicioDeSesion()
                  
            elif opcion == "2":
                print("\n[Registrar cliente seleccionado]")
                
            elif opcion == "3":
                break
            else:
                print("\nOpción no válida. Por favor, intente de nuevo.")
 
    def inicioDeSesion(self):

        print  ("\nDigite 1 para cliente o 2 para admin")
        opcion = input("\nDigite la opción que desea realizar: ").strip()
        if opcion == "1":

         print("\n--- Inicio de Sesión ---")
         id_cliente = input("Ingrese su ID de cliente: ").strip()
         clave = input("Ingrese su clave: ").strip()
        
         if self.auth is None:
          print("El sistema de autenticacion no se ha inicializado.")
          print("Por favor, contacte al administrador.")
          return 
    
         resultado, self.cliente_actual = self.auth.autenticar(id_cliente, clave)

        
         if resultado == "EXITO" and self.cliente_actual is not None:
            
            print(f"\n¡Bienvenido, {self.cliente_actual.nombre}!") 
            self.menuCliente()
            

         elif resultado == "CLAVE_INCORRECTA":

            print("\nClave incorrecta. Por favor, intente de nuevo.")

         elif resultado == "CLIENTE_NO_ENCONTRADO":

            print("\nID de cliente no encontrado. Por favor, registrese primero.")
            
         else:
            print("\nError desconocido durante la autenticación.")

        if opcion == "2":
         print("\n--- Inicio de Sesión Admin ---")
         id_admin = input("Ingrese su ID de admin: ").strip()
         clave_admin = input("Ingrese su clave: ").strip()
        
         if id_admin == "admin" and clave_admin == "admin123":
            print("\n¡Bienvenido, Admin!")
            self.menuAdmin()
         else:
            print("\nCredenciales de admin incorrectas. Por favor, intente de nuevo.")
 

    def cargarDatos(self):
      
        # 1. Usamos  CSVManager para llenar la lista de clientes.
        self.clientes = CSVManager.cargar_clientes("clientes.csv")
        
        self.tickets = CSVManager.cargar_tickets("tickets.csv")

        self.eventos = CSVManager.cargar_eventos("eventos.csv")
        
        # 2. Creamos la instancia de Auth con la lista de clientes ya cargada.
        self.auth = Auth(self.clientes)
        
        # para saber cuantos clientes se cargaron
        print(f"¡Listo! Se cargaron {len(self.clientes)} clientes.")
        # para saber cuantos tiquetes se cargaron
        print(f"¡Listo! Se cargaron {len(self.tickets)} tiquetes.")
        

    def menuAdmin(self):
        print("\n--- Menú Admin ---")
        print("1 - Ver todos los clientes")
        print("2 - Buscar cliente por ID y sus tiquetes")
        print("3 - Agregar evento")
        print("4 - Cerrar sesión")
        opcion = input("\nSeleccione una opción: ").strip()
        if opcion == "1":
         print("\n--- Lista de Clientes ---")
         self.verTodosLosClientes()
        
        elif opcion == "2":
           self.buscarClientePorIDYtiques()
      
        elif opcion == "3":
            #self.agregarEvento()
              print("No implementado aun")
        elif opcion == "4":
           # self.cliente_actual = None
            print("\nSesión de admin cerrada.")
        else:
            print("\nOpción no válida. Por favor, intente de nuevo.")

    def verTodosLosClientes(self):
        for cliente in self.clientes:
            print(cliente)

   
    def buscarClientePorIDYtiques(self):
        id_buscar = input("Ingrese el ID del cliente a buscar: ").strip()

    # 1. Inicializamos las variables ANTES de los bucles.
        cliente_encontrado = None
    
    # 2. Buscamos al cliente. Si lo encontramos, lo guardamos y rompemos el bucle.
        for cliente in self.clientes:
            if cliente.id_cliente == id_buscar:
             cliente_encontrado = cliente
             break
            
    # 3. SI NO SE ENCUENTRA el cliente, informamos y terminamos la función con 'return'.
        if not cliente_encontrado:
         print("\nCliente no encontrado.")
         return # Esto detiene la ejecución de la función aquí mismo.

    # 4. Si llegamos aquí, es porque el cliente SÍ se encontró. Lo mostramos.
        print(f"\nCliente encontrado: {cliente_encontrado}")
    
    # 5. Buscamos y guardamos TODOS los tiquetes del cliente en una nueva lista.
        tickets_del_cliente = []
        for ticket in self.tickets:
            if ticket.id_cliente == id_buscar:
             tickets_del_cliente.append(ticket)
            
    # 6. Al final, revisamos si la lista de tiquetes tiene algo o está vacía.
        if tickets_del_cliente: # Esto es True si la lista no está vacía
            print("Tiquetes encontrados para este cliente:")
            for ticket in tickets_del_cliente:
                print(ticket) # Imprimimos cada tiquete encontrado
        else: # Si la lista está vacía
            print("No se encontraron tiquetes para este cliente.")




    def menuCliente(self):
        print("\n--- Menú Cliente ---")
        print("1 - Ver todos los eventos")
        print("2 - Buscar evento por ID")
        print("3 - Comprar tiquete")
        print("4 - Ver mis tiquetes")
        print("5 - Cerrar sesión")
        opcion = input("\nSeleccione una opción: ").strip()
        if opcion == "1":
            self.verTodosLosEventos()
        elif opcion == "2":
           # self.buscarEventoPorID()
           print("No implementado aun")
        elif opcion == "3":
            #self.comprarTiquete()
                print("No implementado aun")
        elif opcion == "4":
           # self.verMisTiquetes()
             print("No implementado aun")
        elif opcion == "5":
            self.cliente_actual = None
            print("\nSesión cerrada.")
            self.mostraMenuPrincipal()
        else:
            print("\nOpción no válida. Por favor, intente de nuevo.")

    def verTodosLosEventos(self):
        print("\n--- Lista de Eventos ---")
        for evento in self.eventos:
            print(evento)

    
    


