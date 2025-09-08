from datetime import datetime #para mostrar la fecha actual 

class Ticket:
    def __init__(self, id_ticket, id_evento, id_cliente, sector, precio, estado="Activo", fecha_compra=None):
        self.id_ticket = id_ticket
        self.id_evento = id_evento
        self.id_cliente = id_cliente
        self.sector = sector
        self.precio = precio
        self.estado = estado
        self.fecha_compra = fecha_compra if fecha_compra else datetime.now().strftime("%Y-%m-%d")
        
        
           
    def __str__(self):
        return (f"Ticket {self.id_ticket} | Evento: {self.id_evento} | Cliente: {self.id_cliente} | " f"Sector: {self.sector} | Precio: ${self.precio} | Estado: {self.estado} | Fecha: {self.fecha_compra}")
    
    def crear_ticket(self, ticket):
        pass 
    
    
    def actualizar_ticket(self, id_ticket, ):
        pass
    
    def eliminar_ticket(self, id_ticket):
        pass
    
    def listar_tickets(self):
        pass 