from Ticket import Ticket
from CSVManager import CSVManager
from Config import Config
from Operacion import Operacion
from datetime import datetime  # para mostrar la fecha y tiempo actual 

class GestorTicket:
    def __init__(self):
        self.tickets = []
        self.pila_undo = []   # pila de operaciones
        # ✅ ahora se cargan los tickets desde CSVManager
        self.tickets = CSVManager.cargarTickets(Config.ARCHIVO_TICKETS)

    # generar ID automático
    def generar_id_ticket(self):
        if not self.tickets:
            return "T0000001"
        ultimo_id = max(int(t.id_ticket[1:]) for t in self.tickets if t.id_ticket.startswith("T"))
        nuevo_num = ultimo_id + 1
        return f"T{nuevo_num:07d}"   # siempre con 7 dígitos

    # CREATE
    def crear_ticket(self, ticket):
        if not ticket.id_ticket:
            ticket.id_ticket = self.generar_id_ticket()

        if any(t.id_ticket == ticket.id_ticket for t in self.tickets):
            print("Error: Ya existe un ticket con ese ID.")
            return False

        self.tickets.append(ticket)
        CSVManager.guardarTickets(self.tickets, Config.ARCHIVO_TICKETS)  # ✅

        # Registrar en pila para Undo 
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
        CSVManager.guardarTickets(self.tickets, Config.ARCHIVO_TICKETS)  # ✅

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

            CSVManager.guardarTickets(self.tickets, Config.ARCHIVO_TICKETS)  # ✅

            # Registrar en pila para Undo
            self.pila_undo.append(Operacion("actualizar", ticket, datos_extra=estado_anterior))
            return True
        return False

    # DELETE
    def eliminar_ticket(self, id_ticket):
        ticket = self.obtener_ticket(id_ticket)
        if ticket:
            self.tickets.remove(ticket)
            CSVManager.guardarTickets(self.tickets, Config.ARCHIVO_TICKETS)  # ✅

            # Registrar en pila para Undo
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
        CSVManager.guardarTickets(self.tickets, Config.ARCHIVO_TICKETS)  # ✅
        return True
    
    #----------------------------------------------------------------------------------------------------------------
    
    def comprar_ticket(self, cliente, evento, sector):
        """Compra un ticket para un cliente autenticado en un sector específico"""
    
        # Normalizar sector 
        sector = sector.strip().lower()
        if sector == "vip":
            sector = "VIP"
        elif sector == "graderia":
            sector = "Graderia"
        elif sector == "gramilla":
            sector = "Gramilla"
        
        # Validar sector
        if sector not in Config.SECTORES:
            print(f"Error: sector inválido. Debe ser uno de {Config.SECTORES}")
            return False

        # Verificar disponibilidad
        disponibles = evento.capacidades.get(sector, 0)
        if disponibles <= 0:
            print(f"No hay cupos disponibles en {sector} para el evento {evento.nombre}.")
            return False

        # Mostrar disponibilidad
        print(f"Disponibilidad en {sector}: {disponibles} entradas.")

        # Crear ticket
        nuevo_ticket = Ticket(
            id_ticket="",  # se genera automático
            id_evento=evento.id_evento,
            id_cliente=cliente.id_cliente,
            sector=sector,
            precio=evento.precios[sector],
            estado="emitido",
            fecha_compra=datetime.now().strftime("%Y-%m-%d")
        )
        self.crear_ticket(nuevo_ticket)

        # Reducir cupo en el evento
        evento.capacidades[sector] -= 1

        # Cargar todos los eventos existentes
        eventos = CSVManager.cargar_eventos()
        
        # Reemplazar el evento comprado con el actualizado
        for i, ev in enumerate(eventos):
            if ev.id_evento == evento.id_evento:
                eventos[i] = evento
                break

        # Guardar de nuevo todos los eventos
        fieldnames = [
            "id_evento","nombre","fecha_iso",
            "cap_grad","cap_gram","cap_vip",
            "precio_grad","precio_gram","precio_vip"
        ]
        filas = [e.to_dict() for e in eventos]
        CSVManager.guardar_csv(Config.ARCHIVO_EVENTOS, fieldnames, filas)  # ✅

        print(f"✓ Ticket comprado con éxito: {nuevo_ticket}")
        return True
