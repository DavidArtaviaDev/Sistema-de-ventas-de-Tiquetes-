import csv
import os
from Evento import Evento
from Cliente import Cliente
from Ticket import Ticket




class CSVManager:
    # ===========================
    # MÉTODOS PARA TICKETS
    # ===========================
    @staticmethod
    def cargarTickets(filename="tickets.csv"):
        """Carga los tickets desde un archivo CSV y devuelve lista de Ticket"""
        fieldnames = ["id_ticket", "id_evento", "id_cliente", "sector", "precio", "estado", "fecha_compra"]
        filas = CSVManager.cargar_csv(filename, fieldnames)
        tickets = []
        for fila in filas:
            try:
                ticket = Ticket(
                    fila["id_ticket"],
                    fila["id_evento"],
                    fila["id_cliente"],
                    fila["sector"],
                    float(fila["precio"]),
                    fila["estado"],
                    fila["fecha_compra"]
                )
                tickets.append(ticket)
            except (ValueError, KeyError) as e:
                print(f"Error al cargar ticket: {e}")
        return tickets

    @staticmethod
    def guardarTickets(tickets, filename="tickets.csv"):
        """Guarda la lista de Ticket en el archivo CSV"""
        fieldnames = ["id_ticket", "id_evento", "id_cliente", "sector", "precio", "estado", "fecha_compra"]
        filas = []
        for ticket in tickets:
            filas.append({
                "id_ticket": ticket.id_ticket,
                "id_evento": ticket.id_evento,
                "id_cliente": ticket.id_cliente,
                "sector": ticket.sector,
                "precio": str(ticket.precio),
                "estado": ticket.estado,
                "fecha_compra": ticket.fecha_compra
            })
        CSVManager.guardar_csv(filename, fieldnames, filas)

    # ===========================
    # MÉTODOS PARA EVENTOS
    # ===========================
    @staticmethod
    def guardar_eventos(evento, filename="eventos.csv"):
        existe = os.path.exists(filename)
        with open(filename, "a", newline="", encoding="utf-8") as file:
            fieldnames = ["id_evento","nombre","fecha_iso","cap_grad","cap_gram","cap_vip",
                          "precio_grad","precio_gram","precio_vip"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if not existe or os.path.getsize(filename) == 0:
                writer.writeheader()
            writer.writerow(evento.to_dict())

    @staticmethod
    def cargar_eventos(filename="eventos.csv"):
        eventos = []
        try:
            with open(filename, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    try:
                        evento = Evento(
                            row["id_evento"], row["nombre"], row["fecha_iso"],
                            row["cap_grad"], row["cap_gram"], row["cap_vip"],
                            row["precio_grad"], row["precio_gram"], row["precio_vip"]
                        )
                        eventos.append(evento)
                    except Exception:
                        continue
        except FileNotFoundError:
            print(f"No se encontró {filename}")
        return eventos

    # ===========================
    # MÉTODOS PARA CLIENTES
    # ===========================
    @staticmethod
    def guardar_clientes(cliente, filename="clientes.csv"):
        existe = os.path.exists(filename)
        with open(filename, "a", newline="", encoding="utf-8") as file:
            fieldnames = ["id_cliente","nombre","es_platinum","hash_clave"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if not existe or os.path.getsize(filename) == 0:
                writer.writeheader()
            writer.writerow(cliente.to_dict())

    @staticmethod
    def cargar_clientes(filename="clientes.csv"):
        clientes = []
        try:
            with open(filename, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    platinum_str = "si" if row["es_platinum"].lower() == "true" else "no"
                    cliente = Cliente(row["id_cliente"], row["nombre"], platinum_str, "dummy")
                    cliente.hash_clave = row["hash_clave"]
                    clientes.append(cliente)
        except FileNotFoundError:
            print(f"No se encontró {filename}")
        return clientes


    # ===========================
    # UTILIDADES GENERALES
    # ===========================
    @staticmethod
    def obtener_ultimo_id_evento(filename="eventos.csv"):
        with open(filename, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            ids = [row["id_evento"] for row in reader]
            last_id = ids[-1]
            numero = int(last_id[1:]) + 1
            return f"E{numero:03d}"

    
   
    @staticmethod
    def obtener_ultimo_id_cliente(filename="clientes.csv"):
        with open(filename, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            ids = [row["id_cliente"] for row in reader]
            last_id = ids[-1]
            numero = int(last_id[1:]) + 1
            return f"C{numero:04d}"

    @staticmethod
    def cargar_csv(ruta, fieldnames):
        """Lee un archivo CSV y devuelve lista de diccionarios."""
        filas = []
        try:
            with open(ruta, mode="r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if all(campo in row for campo in fieldnames):
                        filas.append(row)
                    else:
                        print(f"Fila corrupta en {ruta}: {row}")
        except FileNotFoundError:
            print(f"Archivo {ruta} no encontrado. Se creará al guardar.")
        return filas

    @staticmethod
    def guardar_csv(ruta, fieldnames, filas):
        """Escribe una lista de diccionarios en un archivo CSV."""
        with open(ruta, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for fila in filas:
                writer.writerow(fila)


    @staticmethod
    def mostrar_eventos(eventos=None, filename="eventos.csv"):
        """Muestra eventos por consola."""
        if eventos is None:
            eventos = CSVManager.cargar_eventos(filename)
        if not eventos:
            print("No hay eventos disponibles.")
            return
        print("\n--- EVENTOS DISPONIBLES ---")
        for i, e in enumerate(eventos, 1):
            print(f"{i}. {e}")


    @staticmethod
    def cargar_tickets(filename="tickets.csv"):
        tickets = []
        try:
            with open(filename, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    try:
                        ticket = Ticket(
                            row["id_ticket"], row["id_evento"], row["id_cliente"],
                            row["sector"], float(row["precio"]), row["estado"],
                            row["fecha_compra"]
                        )
                        tickets.append(ticket)
                    except (ValueError, KeyError) as e:
                        print(f"Error al procesar fila de ticket: {e}")
        except FileNotFoundError:
            print(f"Archivo de tickets no encontrado: {filename}")
        
        return tickets

