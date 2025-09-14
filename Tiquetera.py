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
        print("2 - Ordenar eventos por criterio")
        print("3 - Comprar tiquete")
        print("4 - Ver mis tiquetes")
        print("5 - Cerrar sesión")
        opcion = input("\nSeleccione una opción: ").strip()
        if opcion == "1":
            self.verTodosLosEventos()
        elif opcion == "2":
        
            self.menuOrdenarEventos()

        elif opcion == "3":
            print("No implementado aun")

        elif opcion == "4":
            print("No implementado aun")
           
        elif opcion == "5":
           
            print("\nSesión cerrada.")
            self.cliente_actual = None
            self.mostraMenuPrincipal()

        else:
            print("\nOpción no válida. Por favor, intente de nuevo.")

    def verTodosLosEventos(self):
        print("\n--- Lista de Eventos ---")
        for evento in self.eventos:
            print(evento)

    





    # ordenaientos quicksort y mergesort
    def menuOrdenarEventos(self):
        print("\n--- Menú de Ordenamiento de Eventos ---")
        print("1 - Quicksort")
        print("2 - Mergesort")
        print("3 - Volver al menú anterior")
        opcion = input("\nSeleccione una opción: ").strip()
        
        if opcion == "1":
            print("No implementado aun")
        
        elif opcion == "2":
            print("\nCriterios disponibles para ordenar:")
            print("1 - id_evento")
            print("2 - nombre")
            print("3 - fecha_iso")
            print("4 - cap_grad")
            print("5 - cap_gram")
            print("6 - cap_vip")
            print("7 - precio_grad")
            print("8 - precio_gram")
            print("9 - precio_vip")
            opcion_criterio = input("Seleccione un criterio: ").strip()
            if opcion_criterio == "1":
                criterio = "id_evento"
            elif opcion_criterio == "2":
                criterio = "nombre"
            elif opcion_criterio == "3":
                criterio = "fecha_iso"
            elif opcion_criterio == "4":
                criterio = "cap_grad"
            elif opcion_criterio == "5":
                criterio = "cap_gram"
            elif opcion_criterio == "6":
                criterio = "cap_vip"
            elif opcion_criterio == "7":
                criterio = "precio_grad"
            elif opcion_criterio == "8":
                criterio = "precio_gram"
            elif opcion_criterio == "9":
                criterio = "precio_vip"
            else:
                print("Criterio no válido. Usando 'id_evento' por defecto.")
                criterio = "id_evento"

            eventos_ordenados = self.mergeSortRecursivo(self.eventos, criterio)
            print("\n--- Eventos Ordenados (Mergesort) ---")
            for evento in eventos_ordenados:
                print(evento)


        
        elif opcion == "3":
            return  # Volver al menú anterior
        
        else:
            print("\nOpción no válida. Por favor, intente de nuevo.")

    def mergeSortRecursivo(self,lista: list, criterio: str) -> list:
       
       if len(lista) <= 1:
            return lista
       
       medio = len(lista) // 2
       izquierda = lista[:medio]
       derecha = lista[medio:]

       izquierda_ordenada = self.mergeSortRecursivo(izquierda, criterio)
       derecha_ordenada = self.mergeSortRecursivo(derecha, criterio)
       
       return self.merge(izquierda_ordenada, derecha_ordenada, criterio)    
    
    def merge(self, izquierda: list, derecha: list, criterio: str) -> list:
        resultado = []
        i = j = 0

        while i < len(izquierda) and j < len(derecha):
            valor_izquierda = getattr(izquierda[i], criterio)
            valor_derecha = getattr(derecha[j], criterio)
         
            if valor_izquierda <= valor_derecha:
                resultado.append(izquierda[i])
                i += 1
            else:
                resultado.append(derecha[j])
                j += 1

        resultado.extend(izquierda[i:])
        resultado.extend(derecha[j:])
        return resultado

