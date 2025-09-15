# Es recomendable importar las clases que se usarán para type hinting (opcional pero buena práctica)
from typing import List, Optional
from Auth import Auth
from CSVManager import CSVManager
from Cliente import Cliente
from Evento import Evento
from GestorTicket import GestorTicket
from Config import Config


class Tiquetera:

    # Parte de David

    def __init__(self):
        self.clientes = []
      
        self.cliente_actual = None  # Cliente autenticado actualmente el que esta utilizando la aplicacion en momento
        self.auth = None    # Objeto Auth para manejar autenticaciones se carga en la funcion cargarDatos
        self.eventos = []   # Lista de eventos cargados



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
                #mostrar el menu del cliente autenticado
                if self.cliente_actual is not None:
                   self.mostrarMenuCliente()
                  
                  
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
            # Aquí puedes agregar el menú o funcionalidades específicas para el admin
         else:
            print("\nCredenciales de admin incorrectas. Por favor, intente de nuevo.")
 

    def cargarDatos(self):
      
        # 1. Usamos  CSVManager para llenar la lista de clientes.
        self.clientes = CSVManager.cargar_clientes("clientes.csv")
        
        # 2. Creamos la instancia de Auth con la lista de clientes ya cargada.
        self.auth = Auth(self.clientes)
        
        # para saber cuantos clientes se cargaron
        #print(f"¡Listo! Se cargaron {len(self.clientes)} clientes.")
        
         # 3. Cargamos los eventos desde CSV usando CSVManager
        self.eventos = CSVManager.cargar_eventos(Config.ARCHIVO_EVENTOS)
        print(f" Se cargaron {len(self.clientes)} clientes y {len(self.eventos)} eventos.")

    def menuAdmin(self):
        print("\n--- Menú Admin ---")
        print("1 - Ver todos los clientes")
        print("2 - Buscar cliente por ID")
        print("3 - Agregar evento")
        print("4 - Cerrar sesión")
        opcion = input("\nSeleccione una opción: ").strip()

    
    """"
    def cargar_eventos(self):
        "Carga eventos desde CSV en memoria"
        filas = CSVManager.cargar_csv(Config.ARCHIVO_EVENTOS, [
            "id_evento","nombre","fecha_iso",
            "cap_grad","cap_gram","cap_vip",
            "precio_grad","precio_gram","precio_vip"
        ])
        self.eventos = [] #lista vacia para almacenar los elementos de evemto que se vana crear 
        for fila in filas: #para ir fila por fila del csv 
            try:
                evento = Evento( #objeto 
                    fila["id_evento"], fila["nombre"], fila["fecha_iso"],
                    int(fila["cap_grad"]), int(fila["cap_gram"]), int(fila["cap_vip"]),
                    int(fila["precio_grad"]), int(fila["precio_gram"]), int(fila["precio_vip"])
                )
                self.eventos.append(evento) # se guarda el onjeto en la lista self.eventos, para luego mostralo 
            except Exception as e:
                print(f"Error cargando evento: {e}")
"""
    """def mostrar_eventos(self):
        #Lista todos los eventos disponibles
        if not self.eventos: #aqui se compruba si la lista esta vacia o no 
            print("No hay eventos disponibles.")
            return
        print("\n--- EVENTOS DISPONIBLES ---")
        for i, e in enumerate(self.eventos, 1): #recorre la lista 
            print(f"{i}. {e}") #devuleve el  indice i y el onjeto e que trae el string con toda la info de eventos 
"""
    def mostrarMenuCliente(self):
        """Menú interactivo del cliente autenticado"""
        if self.cliente_actual is None:
            print("Debe iniciar sesión primero.")
            return

        gestor_tickets = GestorTicket()

        while True:
            print("\n--- MENÚ CLIENTE ---")
            print("1 - Ver mis entradas")
            print("2 - Comprar entradas")
            print("3 - Cerrar sesión")
            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                print("\n--- MIS TICKETS ---")
                encontrados = False
                for t in gestor_tickets.tickets:
                    if t.id_cliente == self.cliente_actual.id_cliente:
                        print(t)
                        encontrados = True
                if not encontrados:
                    print("No tienes entradas registradas.")

            elif opcion == "2":
                # 🔧 FIX: aquí antes estaba mal llamado
                CSVManager.mostrar_eventos(self.eventos)
                if not self.eventos:
                    continue

                try:
                    idx_evento = int(input("Número del evento: ")) - 1
                    evento_seleccionado = self.eventos[idx_evento]
                except (ValueError, IndexError):
                    print("Selección inválida.")
                    continue

                print("\nSectores disponibles:")
                for sector, cupo in evento_seleccionado.capacidades.items():
                    print(f"- {sector}: {cupo} entradas")

                sector = input("Seleccione sector: ").capitalize()
                gestor_tickets.comprar_ticket(self.cliente_actual, evento_seleccionado, sector)

            elif opcion == "3":
                print("Cerrando sesión...")
                self.cliente_actual = None
                break

            else:
                print("Opción inválida, intente de nuevo.")
        

   