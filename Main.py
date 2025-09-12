
































































































































from Ticket import Ticket
from GestorTicket import GestorTicket

def menu():
    gestor = GestorTicket()

    while True:
        print("\n=== MENU GESTION DE TICKETS ===")
        print("1. Crear ticket")
        print("2. Listar tickets")
        print("3. Buscar ticket por ID")
        print("4. Actualizar ticket")
        print("5. Cancelar ticket")
        print("6. Eliminar ticket")
        print("7. Deshacer ultima operacion")
        print("0. Salir")

        opcion = input("Seleccione una opcion: ")

        if opcion == "1":
            id_evento = input("ID del evento: ")
            id_cliente = input("ID del cliente: ")
            sector = input("Sector (Graderia/Gramilla/VIP): ")
            precio = input("Precio: ")

            try:
                ticket = Ticket("", id_evento, id_cliente, sector, precio)
                if gestor.crear_ticket(ticket):
                    print(f"Ticket creado con ID {ticket.id_ticket}")
            except ValueError as e:
                print(f"Error: {e}")

        elif opcion == "2":
            gestor.listar_tickets()

        elif opcion == "3":
            id_ticket = input("Ingrese el ID del ticket: ")
            ticket = gestor.obtener_ticket(id_ticket)
            if ticket:
                print(ticket)
            else:
                print("Ticket no encontrado.")

        elif opcion == "4":
            id_ticket = input("Ingrese el ID del ticket a actualizar: ")
            campo = input("Campo a actualizar (sector/precio/estado): ")
            nuevo_valor = input(f"Nuevo valor para {campo}: ")

            # Conversión de precio a float si corresponde
            if campo == "precio":
                try:
                    nuevo_valor = float(nuevo_valor)
                except ValueError:
                    print("Error, el precio debe ser numerico.")
                    continue

            if gestor.actualizar_ticket(id_ticket, **{campo: nuevo_valor}):
                print( "Ticket actualizado.")
            else:
                print("No se pudo actualizar el ticket.")

        elif opcion == "5":
            id_ticket = input("Ingrese el ID del ticket a cancelar: ")
            gestor.cancelar_ticket(id_ticket)

        elif opcion == "6":
            id_ticket = input("Ingrese el ID del ticket a eliminar: ")
            if gestor.eliminar_ticket(id_ticket):
                print("Ticket eliminado.")
            else:
                print("Ticket no encontrado.")

        elif opcion == "7":
            gestor.deshacer()

        elif opcion == "0":
            print("Fuera de sistema")
            break

        else:
            print("Opcion invalida.")

if __name__ == "__main__":
    menu()
