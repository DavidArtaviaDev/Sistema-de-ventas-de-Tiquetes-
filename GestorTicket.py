from Ticket import Ticket
from CSVManager import CSVManager
from Config import Config
from Operacion import Operacion

class GestorTicket:
    def __init__(self):
        self.tickets = []
        self.pila_undo = []   # pila de operaciones
        self.cargar_csv()


    
    
    def cargar_csv(self):
        """Carga los tickets desde el archivo CSV"""
        fieldnames = ["id_ticket", "id_evento", "id_cliente", "sector", "precio", "estado", "fecha_compra"]
        filas = CSVManager.cargar_csv(Config.ARCHIVO_TICKETS, fieldnames)
        
        self.tickets = []
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
                self.tickets.append(ticket)
            except (ValueError, KeyError) as e:
                print(f"Error al cargar ticket: {e}")

    def guardar_csv(self):
        """Guarda los tickets en el archivo CSV"""
        fieldnames = ["id_ticket", "id_evento", "id_cliente", "sector", "precio", "estado", "fecha_compra"]
        filas = []
        for ticket in self.tickets:
            fila = {
                "id_ticket": ticket.id_ticket,
                "id_evento": ticket.id_evento,
                "id_cliente": ticket.id_cliente,
                "sector": ticket.sector,
                "precio": str(ticket.precio),
                "estado": ticket.estado,
                "fecha_compra": ticket.fecha_compra
            }
            filas.append(fila)
        
        CSVManager.guardar_csv(Config.ARCHIVO_TICKETS, fieldnames, filas)
   
    # generar ID automático, no sé como funciona 
    def generar_id_ticket(self):
        if not self.tickets:
            return "T0001"
        ultimo_id = max(int(t.id_ticket[1:]) for t in self.tickets if t.id_ticket.startswith("T"))
        nuevo_num = ultimo_id + 1
        return f"T{nuevo_num:04d}"

    # CREATE
    def crear_ticket(self, ticket):
        if not ticket.id_ticket:
            ticket.id_ticket = self.generar_id_ticket()

        if any(t.id_ticket == ticket.id_ticket for t in self.tickets):
            print("Error: Ya existe un ticket con ese ID.")
            return False

        self.tickets.append(ticket)
        self.guardar_csv()

        #  Registrar en pila para Undo 
        self.pila_undo.append(Operacion("crear", ticket))
        return True

    # READ
    def obtener_ticket(self, id_ticket):
        for t in self.tickets:
            if t.id_ticket == id_ticket:
                return t
        return None
    
    def cancelar_ticket(self, id_ticket):
        ticket = self.obtener_ticket(id_ticket)
        if not ticket:
            print(f"Error, No se encontro el ticket {id_ticket}")
            return False
        
        if ticket.estado == "Cancelado":
            print(f"El ticket {id_ticket} ya estaba cancelado.")
            return False
        
        # Guardar estado anterior para Undo
        estado_anterior = {"estado": ticket.estado}
        
        # Cancelar ticket
        ticket.cancelar_ticket()
        self.guardar_csv()

        # Registrar operación en la pila Undo
        self.pila_undo.append(Operacion("actualizar", ticket, datos_extra=estado_anterior))
        print(f"Ticket {id_ticket} cancelado con exito.")
        return True

    def listar_tickets(self):
        if not self.tickets:
            print("No hay tickets registrados.")
        else:
            for t in self.tickets:
                print(t)

    # UPDATE
    def actualizar_ticket(self, id_ticket, **kwargs):
        ticket = self.obtener_ticket(id_ticket)
        if ticket:
            # Guardamos estado anterior
            estado_anterior = {key: getattr(ticket, key) for key in kwargs if hasattr(ticket, key)}

            for key, value in kwargs.items():
                if hasattr(ticket, key):
                    setattr(ticket, key, value)

            self.guardar_csv()

            # --- Registrar en pila para Undo ---
            self.pila_undo.append(Operacion("actualizar", ticket, datos_extra=estado_anterior))
            return True
        return False

    # DELETE
    def eliminar_ticket(self, id_ticket):
        ticket = self.obtener_ticket(id_ticket)
        if ticket:
            self.tickets.remove(ticket)
            self.guardar_csv()

            # --- Registrar en pila para Undo ---
            self.pila_undo.append(Operacion("eliminar", ticket))
            return True
        return False

    # metodo para deshacer
    def deshacer(self):
        if not self.pila_undo:
            print("No hay operaciones para deshacer.")
            return False

        ultima_op = self.pila_undo.pop()

        if ultima_op.tipo == "crear":
            # Deshacer creación = eliminar ticket
            self.tickets = [t for t in self.tickets if t.id_ticket != ultima_op.ticket.id_ticket]
            print(f"Deshecha creación del ticket {ultima_op.ticket.id_ticket}")

        elif ultima_op.tipo == "eliminar":
            # Deshacer eliminación = volver a agregar ticket
            self.tickets.append(ultima_op.ticket)
            print(f"Deshecha eliminación del ticket {ultima_op.ticket.id_ticket}")

        elif ultima_op.tipo == "actualizar":
            # Deshacer actualización = restaurar valores anteriores
            for key, value in ultima_op.datos_extra.items():
                setattr(ultima_op.ticket, key, value)
            print(f"Deshecha actualización del ticket {ultima_op.ticket.id_ticket}")

        # Guardar cambios en CSV después de revertir
        self.guardar_csv()
        return True
