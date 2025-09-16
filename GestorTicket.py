from Ticket import Ticket
from CSVManager import CSVManager
from Config import Config
from Operacion import Operacion
from datetime import datetime  # para mostrar la fecha y tiempo actual 

class GestorTicket:
    def __init__(self):
        self.tickets = []
        self.pila_undo = []   # pila de operaciones
        #ahora se cargan los tickets desde CSVManager
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
        CSVManager.guardarTickets(self.tickets, Config.ARCHIVO_TICKETS)  # 
        return True
    
    #----------------------------------------------------------------------------------------------------------------
    
    def comprar_ticket(self, cliente, eventos):
        """Compra un ticket para un cliente autenticado."""
        if not eventos:
            print("No hay eventos disponibles.")
            return False

        # Mostrar eventos
        CSVManager.mostrar_eventos(eventos)
        try:
            idx_evento = int(input("Número del evento que desea comprar: ")) - 1
            evento_seleccionado = eventos[idx_evento]
        except (ValueError, IndexError):
            print("Selección inválida.")
            return False

        # Mostrar sectores disponibles
        print("\nSectores disponibles:")
        for sector, cupo in evento_seleccionado.capacidades.items():
            print(f"- {sector}: {cupo} entradas")

        # Seleccionar sector
        sector = input("Seleccione sector: ").capitalize()

        # Normalizar sector
        sector = sector.strip().lower()
        if sector == "vip":
            sector = "VIP"
        elif sector == "graderia":
            sector = "Graderia"
        elif sector == "gramilla":
            sector = "Gramilla"

        # Validar sector y disponibilidad
        if sector not in Config.SECTORES:
            print(f"Error: sector inválido. Debe ser uno de {Config.SECTORES}")
            return False

        if evento_seleccionado.capacidades.get(sector, 0) <= 0:
            print(f"No hay cupos disponibles en {sector} para el evento {evento_seleccionado.nombre}.")
            return False

        # Crear ticket y actualizar evento
        nuevo_ticket = Ticket(
            id_ticket="",
            id_evento=evento_seleccionado.id_evento,
            id_cliente=cliente.id_cliente,
            sector=sector,
            precio=evento_seleccionado.precios[sector],
            estado="emitido",
            fecha_compra=datetime.now().strftime("%Y-%m-%d")
        )
        self.crear_ticket(nuevo_ticket)
        evento_seleccionado.capacidades[sector] -= 1

        # Guardar eventos actualizados en CSV
        fieldnames = [
            "id_evento","nombre","fecha_iso",
            "cap_grad","cap_gram","cap_vip",
            "precio_grad","precio_gram","precio_vip"
        ]
        filas = [e.to_dict() for e in eventos]
        CSVManager.guardar_csv(Config.ARCHIVO_EVENTOS, fieldnames, filas)

        print(f"Ticket comprado con exito: {nuevo_ticket}")
        return True




    def ver_tickets_cliente(self, cliente):
        """Muestra todos los tickets asociados a un cliente"""
        print("\n--- MIS TICKETS ---")
        encontrados = False
        for t in self.tickets:
            if t.id_cliente == cliente.id_cliente:
                print(t)
                encontrados = True
        if not encontrados:
            print("No tienes entradas registradas.")
