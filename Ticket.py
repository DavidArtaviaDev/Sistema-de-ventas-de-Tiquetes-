from datetime import datetime
from Config import Config

class Ticket:
    def __init__(self, id_ticket, id_evento, id_cliente, sector, precio, estado="emitido", fecha_compra=None):
        if sector not in Config.SECTORES:
            raise ValueError(f"Sector invalido. Debe ser uno de {Config.SECTORES}")
        if estado not in Config.ESTADOS_TICKET:
            raise ValueError(f"Estado invalido. Debe ser uno de {Config.ESTADOS_TICKET}")

        self.id_ticket = id_ticket
        self.id_evento = id_evento
        self.id_cliente = id_cliente
        self.sector = sector
        self.precio = float(precio)
        self.estado = estado
        self.fecha_compra = fecha_compra if fecha_compra else datetime.now().strftime("%Y-%m-%d")

    def __str__(self):
        return (f"Ticket {self.id_ticket} | Evento: {self.id_evento} | Cliente: {self.id_cliente} | "
                f"Sector: {self.sector} | Precio: ${self.precio} | Estado: {self.estado} | Fecha: {self.fecha_compra}")

    def cancelar_ticket(self):
        if self.estado == "Activo":
            self.estado = "Cancelado"
        else:
            print(f"El ticket {self.id_ticket} ya estaba cancelado.")
