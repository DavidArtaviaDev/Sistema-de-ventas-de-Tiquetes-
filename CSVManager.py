
import csv
from Evento import Evento
from Cliente import Cliente
from Ticket import Ticket
import os

class CSVManager:
    @staticmethod
    def guardar_eventos(eventos, filename="eventos.csv"):
        existe = os.path.exists(filename) #comprueba que el archivo exista
        with open(filename, "a", newline="", encoding="utf-8") as file: #abre el archivo en modo append

            fieldnames = ["id_evento","nombre","fecha_iso","cap_grad","cap_gram","cap_vip", #define los nombres de las columnas
                          "precio_grad","precio_gram","precio_vip"]
            
            writer = csv.DictWriter(file, fieldnames=fieldnames) #crea un escritor de diccionarios 
            if not existe or os.path.getsize(filename) == 0: #si el archivo no existe o esta vacio
                writer.writeheader() #escribe la primera fila del CSV con los nombres de las columnas
            writer.writerow(eventos.to_dict()) #escribe los datos del diccionario que estan en la clase evento

    @staticmethod
    def cargar_eventos(filename="eventos.csv"):
        eventos = []
        try:
            with open(filename, "r", encoding="utf-8") as file: #abre el csv en modo lectura
                reader = csv.DictReader(file) #lee cada fila 
                for row in reader: #Por cada fila crea un objeto Evento y lo agrega a la lista eventos
                    try:
                        evento = Evento(
                            row["id_evento"], row["nombre"], row["fecha_iso"],
                            row["cap_grad"], row["cap_gram"], row["cap_vip"],
                            row["precio_grad"], row["precio_gram"], row["precio_vip"]
                        )
                        eventos.append(evento)
                    except Exception:
                        # Si hay algún error con esa fila, simplemente la salta
                        continue
        except FileNotFoundError: #para que el programa no se detenga
            print(f" No se encontró {filename}")
        return eventos

    @staticmethod
    def guardar_clientes(clientes, filename="clientes.csv"):
       existe = os.path.exists(filename)
       with open(filename, "a", newline="", encoding="utf-8") as file:

        fieldnames = ["id_cliente","nombre","es_platinum","hash_clave"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not existe or os.path.getsize(filename) == 0:
            writer.writeheader()
        writer.writerow(clientes.to_dict())

    @staticmethod
    def cargar_clientes(filename="clientes.csv"):
        clientes = []
        try:
            with open(filename, "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    platinum_str = "si" if row["es_platinum"].lower() == "true" else "no"
                    cliente = Cliente(row["id_cliente"], row["nombre"], platinum_str, "dummy")
                    cliente.hash_clave = row["hash_clave"]  # usar el hash ya guardado
                    clientes.append(cliente)

        except FileNotFoundError:
            print(f"No se encontró {filename}")

        return clientes
    
    @staticmethod
    def obtener_ultimo_id_evento(filename="eventos.csv"):
        with open(filename, "r", encoding="utf-8") as file:

             reader = csv.DictReader(file) #abre el csv y lo lee
             ids = [row["id_evento"] for row in reader] #estrae todos los ids
             last_id = ids[-1] #toma el ultimo id
             numero = int(last_id[1:]) + 1 #quita la parte numerica del id y le suma 1
             return f"E{numero:03d}" #devuelve el id con la letra

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
        """Lee un archivo CSV y devuelve una lista de diccionarios."""
        filas = []
        try:
            with open(ruta, mode="r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Validar que tenga todas las columnas esperadas
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