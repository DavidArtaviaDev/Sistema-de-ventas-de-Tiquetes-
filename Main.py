from Evento import Evento
from Cliente import Cliente
from CSVManager import CSVManager

# listas en memoria
eventos = []
clientes = []

def menu():
    while True:
        print("\n=== MENÚ PERSONA 1 (Eventos y Clientes) ===")
        print("1. Agregar evento")
        print("2. Listar eventos")
        print("3. Cargar eventos desde CSV")
        print("4. Registrar cliente")
        print("5. Listar clientes")
        print("6. Cargar clientes desde CSV")
        print("0. Salir")

        opcion = input("Seleccione una opción: ")

        # ---------------- Opción 1: Agregar evento ----------------
        if opcion == "1":
            id_e = CSVManager.obtener_ultimo_id_evento()
            nombre = input("Nombre: ")
            fecha = input("Fecha (YYYY-MM-DD): ")
            cap_grad = input("Capacidad gradería: ")
            cap_gram = input("Capacidad gramilla: ")
            cap_vip = input("Capacidad VIP: ")
            precio_grad = input("Precio gradería: ")
            precio_gram = input("Precio gramilla: ")
            precio_vip = input("Precio VIP: ")
            try:
                evento = Evento(id_e, nombre, fecha, cap_grad, cap_gram, cap_vip,
                                precio_grad, precio_gram, precio_vip)
                eventos.append(evento)                   # guardar en memoria
                CSVManager.guardar_eventos(evento)       # guardar en CSV
                print(f" Evento '{nombre}' agregado y guardado en CSV.")
            except ValueError as e:
                print(f" Error: {e}")

        # ---------------- Opción 2: Listar eventos ----------------
        elif opcion == "2":
            if not eventos:
                print("No hay eventos registrados en memoria.")
            else:
                for e in eventos:
                    print(e)

        # ---------------- Opción 3: Cargar eventos desde CSV ----------------
        elif opcion == "3":
            eventos.clear()
            eventos.extend(CSVManager.cargar_eventos())
            print("Eventos cargados desde CSV.")

        # ---------------- Opción 4: Registrar cliente ----------------
        elif opcion == "4":
            id_c = CSVManager.obtener_ultimo_id_cliente()
            nombre = input("Nombre: ")
            es_plat = input("¿Es Platinum? (si/no): ")
            clave = input("Clave: ")
            try:
                cliente = Cliente(id_c, nombre, es_plat, clave)
                clientes.append(cliente)                   # guardar en memoria
                CSVManager.guardar_clientes(cliente)       # guardar en CSV
                print(f"Cliente '{nombre}' registrado y guardado en CSV.") 
            except ValueError as e:
                print(f"Error: {e}")

        # ---------------- Opción 5: Listar clientes ----------------
        elif opcion == "5":
            if not clientes:
                print("No hay clientes registrados en memoria.")
            else:
                for c in clientes:
                    print(c)

        # ---------------- Opción 6: Cargar clientes desde CSV ----------------
        elif opcion == "6":
            clientes.clear()
            clientes.extend(CSVManager.cargar_clientes())
            print("Clientes cargados desde CSV.")

        # ---------------- Salir ----------------
        elif opcion == "0":
            print("Saliendo...")
            break

        else:
            print("Opción inválida.")

if __name__ == "__main__":
    menu()
