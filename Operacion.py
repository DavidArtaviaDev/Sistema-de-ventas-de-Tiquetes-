class Operacion:
    def __init__(self, tipo, ticket, datos_extra=None):
        """
        tipo: str -> "crear", "eliminar", "actualizar"
        ticket: Ticket -> el ticket involucrado
        datos_extra: dict -> información adicional (ej: valores anteriores)
        """
        self.tipo = tipo
        self.ticket = ticket
        self.datos_extra = datos_extra or {}
