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
        self.eventos = []
        self.tickets = []

        self.cliente_actual = None  # Cliente autenticado actualmente el que esta utilizando la aplicacion en momento
        self.auth = None    # Objeto Auth para manejar autenticaciones se carga en la funcion cargarDatos
        self.eventos = []   # Lista de eventos cargados
        
        # Inicializamos gestor de tickets
        self.gestor_tickets = GestorTicket()



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
                #if self.cliente_actual is not None:
                   # self.mostrarMenuCliente()
        
            elif opcion == "2":
                self.registrarCliente()
                
            elif opcion == "3":
                break
            else:
                print("\nOpción no válida. Por favor, intente de nuevo.")
 

    def registrarCliente(self):
         id_c = CSVManager.obtener_ultimo_id_cliente()
         nombre = input("Nombre: ")
         es_plat = input("¿Es Platinum? (si/no): ")
         clave = input("Clave: ")
         try:
                cliente = Cliente(id_c, nombre, es_plat, clave)
                self.clientes.append(cliente)                   # guardar en memoria
                CSVManager.guardar_clientes(cliente)       # guardar en CSV
                print(f"Cliente '{nombre}' registrado y guardado en CSV.") 
                print("Su ID de cliente es:", id_c)
         except ValueError as e:
                print(f"Error: {e}")



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

        
         # 3. Cargamos los eventos desde CSV usando CSVManager
        #self.eventos = CSVManager.cargar_eventos(Config.ARCHIVO_EVENTOS)
        
        print(f" Se cargaron {len(self.eventos)} eventos.")

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
              self.crearEventoNuevo()  
              
        elif opcion == "4":
           # self.cliente_actual = None
            print("\nSesión de admin cerrada.")
        else:
            print("\nOpción no válida. Por favor, intente de nuevo.")


    
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
    """def mostrarMenuCliente(self)
        Menú interactivo del cliente autenticado
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
        
"""
   

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

    def crearEventoNuevo(self):
        """
        Pide al usuario los datos para un nuevo evento, lo crea,
        lo añade a la lista en memoria y lo guarda en el CSV.
        """
        print("\n--- Creando Nuevo Evento ---")
        try:
            # Obtenemos los datos del usuario
            # (Asumo que CSVManager.obtener_ultimo_id_evento existe y funciona)
            id_e = CSVManager.obtener_ultimo_id_evento()
            nombre = input("Nombre del evento: ")
            fecha = input("Fecha (YYYY-MM-DD): ")
            cap_grad = input("Capacidad gradería: ")
            cap_gram = input("Capacidad gramilla: ")
            cap_vip = input("Capacidad VIP: ")
            precio_grad = input("Precio gradería: ")
            precio_gram = input("Precio gramilla: ")
            precio_vip = input("Precio VIP: ")

            # Creamos la instancia del Evento (esto puede fallar si los datos son inválidos)
            evento = Evento(id_e, nombre, fecha, cap_grad, cap_gram, cap_vip,
                            precio_grad, precio_gram, precio_vip)
            
            # Usamos self.eventos, el atributo de la clase
            self.eventos.append(evento)
            
            # Guardamos en el archivo CSV (tu método parece guardar de uno en uno)
            CSVManager.guardar_eventos(evento)
            
            print(f"\n¡Éxito! Evento '{nombre}' agregado y guardado.")

        except ValueError as e:
            # Capturamos los errores de validación del constructor de Evento
            print(f"\nError al crear el evento: {e}")
        except Exception as e:
            # Capturamos cualquier otro error inesperado
            print(f"\nOcurrió un error inesperado: {e}")


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
            self.gestor_tickets.comprar_ticket(self.cliente_actual, self.eventos)
        

        elif opcion == "4":
            self.gestor_tickets.ver_tickets_cliente(self.cliente_actual)
           
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
        
        if opcion == "1":
            eventos_ordenados = self.quick_sort_eventos(criterio)
            print("\n--- Eventos Ordenados (Quicksort) ---")
            for evento in eventos_ordenados:
                print(evento)
        
        elif opcion == "2":
         

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

    def quick_sort_eventos(self, criterio: str) -> list:
        """
        Ordena una copia de la lista de eventos usando QuickSort.
        Este es el método público que se debe llamar.
        """
        # 1. Creamos una copia para no modificar self.eventos
        lista_a_ordenar = list(self.eventos)
        
        # 2. Llamamos al método recursivo para que ordene la copia
        self._quick_sort_recursivo(lista_a_ordenar, 0, len(lista_a_ordenar) - 1, criterio)
        
        # 3. Devolvemos la copia ya ordenada
        return lista_a_ordenar

    def _quick_sort_recursivo(self, lista: list, bajo: int, alto: int, criterio: str):
        """
        Método auxiliar recursivo que implementa la lógica de "Divide y Vencerás".
        'bajo' y 'alto' son los índices que definen la sublista actual.
        """
        if bajo < alto:
            # Encuentra el índice del pivote, que ya estará en su lugar correcto
            pivote_idx = self._partition(lista, bajo, alto, criterio)

            # Llama recursivamente al método para las dos sublistas
            # (elementos antes del pivote y elementos después del pivote)
            self._quick_sort_recursivo(lista, bajo, pivote_idx - 1, criterio)
            self._quick_sort_recursivo(lista, pivote_idx + 1, alto, criterio)

    def _partition(self, lista: list, bajo: int, alto: int, criterio: str) -> int:
        """
        Toma el último elemento como pivote, lo coloca en su posición ordenada
        y pone todos los elementos más pequeños a su izquierda y los más grandes a su derecha.
        """
        # 1. Elegimos el último elemento de la sublista como nuestro pivote
        pivote = getattr(lista[alto], criterio)
        
        # 'i' es el índice del último elemento que era más pequeño que el pivote
        i = bajo - 1

        # 2. Recorremos la sublista desde el inicio ('bajo') hasta justo antes del pivote
        for j in range(bajo, alto):
            # Si el elemento actual es menor o igual que el pivote...
            if getattr(lista[j], criterio) <= pivote:
                # ...incrementamos 'i' y lo intercambiamos con el elemento en la posición 'j'
                i += 1
                lista[i], lista[j] = lista[j], lista[i]

        # 3. Al final del bucle, todos los elementos hasta 'i' son menores que el pivote.
        # Ahora, colocamos el pivote en su lugar correcto (justo después del último elemento menor)
        lista[i + 1], lista[alto] = lista[alto], lista[i + 1]
        
        # 4. Devolvemos el índice donde quedó el pivote
        return i + 1

