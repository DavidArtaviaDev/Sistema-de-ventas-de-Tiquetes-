# Es recomendable importar las clases que se usarán para type hinting (opcional pero buena práctica)
from typing import List, Optional
from Auth import Auth
from CSVManager import CSVManager
from Cliente import Cliente
from Evento import Evento

class Tiquetera:

    # Parte de David

    def __init__(self):
        self.clientes = []
      
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
                #mostrar el menu del cliente autenticado
                #if self.cliente_actual is not None:
                   # self.mostrarMenuCliente()
                  
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
        print(f"¡Listo! Se cargaron {len(self.clientes)} clientes.")
        

    def menuAdmin(self):
        print("\n--- Menú Admin ---")
        print("1 - Ver todos los clientes")
        print("2 - Buscar cliente por ID")
        print("3 - Agregar evento")
        print("4 - Cerrar sesión")
        opcion = input("\nSeleccione una opción: ").strip()

     