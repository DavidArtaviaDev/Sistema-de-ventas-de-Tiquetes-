import heapq
from Ticket import Ticket
from datetime import datetime

class SolicitudCompra:
    def __init__(self, cliente, evento, sector, cantidad):
        self.cliente = cliente
        self.evento = evento
        self.sector = sector
        self.cantidad = cantidad
        self.cola_tickets = []  # lista en lugar de PriorityQueue

    def agregar_ticket(self, ticket):
        # Platinum → prioridad 0, Normal → 1
        prioridad = 0 if self.cliente.es_platinum else 1
        self.cola_tickets.append((prioridad, datetime.now(), ticket))
        # siempre mantenemos ordenada la lista
        self.cola_tickets.sort(key=lambda x: (x[0], x[1]))

    def obtener_tickets(self):
        # devuelve los tickets en orden de prioridad y llegada
        tickets = [ticket for _, _, ticket in self.cola_tickets]
        self.cola_tickets.clear()  # vaciar la cola después de procesar
        return tickets

    def __str__(self):
        return f"Solicitud de {self.cliente.nombre} ({'Platinum' if self.cliente.es_platinum else 'Normal'}) - {self.cantidad} tickets en {self.sector} para {self.evento.nombre}"



    def recibirTicketsPorSector(self):
        if not self.solicitudes:
            print("No hay solicitudes pendientes.")
            return

        id_evento = input("Ingrese el código del evento: ").strip()
        solicitudes_evento = [s for s in self.solicitudes if s.evento.id_evento == id_evento]

        if not solicitudes_evento:
            print("No hay solicitudes para este evento.")
            return

        print("\nSectores disponibles para este evento:")
        sectores = list({s.sector for s in solicitudes_evento})
        for i, sec in enumerate(sectores, start=1):
            print(f"{i}. {sec}")

        try:
            idx_sec = int(input("Seleccione el sector: ")) - 1
            sector_seleccionado = sectores[idx_sec]
        except (ValueError, IndexError):
            print("Selección inválida.")
            return

        # Filtrar solicitudes del sector
        solicitudes_sector = [s for s in solicitudes_evento if s.sector == sector_seleccionado]

        if not solicitudes_sector:
            print(f"No hay solicitudes en el sector {sector_seleccionado}.")
            return

        # Ordenar sectores por prioridad VIP > Gramilla > Graderia
        orden_sectores = {"VIP": 0, "Gramilla": 1, "Graderia": 2}

        tickets = []
        for solicitud in solicitudes_sector:
            tickets.extend(solicitud.obtener_tickets())

        # ordenar tickets por sector
        tickets.sort(key=lambda t: orden_sectores.get(t.sector, 99))

        print(f"\n--- Tickets en {sector_seleccionado} para el evento {id_evento} ---")
        for t in tickets:
            print(t)
