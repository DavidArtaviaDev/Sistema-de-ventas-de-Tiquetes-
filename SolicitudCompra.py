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
