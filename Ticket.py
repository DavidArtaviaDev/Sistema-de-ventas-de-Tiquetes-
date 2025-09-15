from datetime import datetime
from Config import Config

class Ticket:
    def __init__(self, id_ticket, id_evento, id_cliente, sector, precio, estado="emitido", fecha_compra=None):
        # Normalizar del sector, strip se encarga de los espacio y lower para las mayuscula 
        sector = sector.strip()
        if sector.lower() == "vip": #luego estos comparan las minusculas cn la que ya viene en Config.py 
            sector = "VIP"
        elif sector.lower() == "graderia":
            sector = "Graderia"
        elif sector.lower() == "gramilla":
            sector = "Gramilla"
            
        if sector not in Config.SECTORES:#Valida que los sectores que se estan ingresando sean igual a los de Config.py 
            raise ValueError(f"Sector invalido. Debe ser uno de {Config.SECTORES}")
        if estado not in Config.ESTADOS_TICKET: #valida que los Tickets que entran esten en estado de "emitido" de lo contrario sale estado invalido 
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

    #def cancelar_ticket(self):
        if self.estado == "emitido":
            pass
            #self.estado = "Cancelado"
        else:
            print(f"El ticket {self.id_ticket} ya estaba cancelado.")
