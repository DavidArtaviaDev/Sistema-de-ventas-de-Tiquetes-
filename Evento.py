# Clase Evento para el sistema de tiquetera
class Evento:
	def __init__(self, id_evento: str, nombre: str, fecha_iso: str, capacidades: dict, precios: dict):
		self.id_evento = id_evento  # str: ID único del evento
		self.nombre = nombre        # str: Nombre del evento
		self.fecha_iso = fecha_iso  # str: Fecha en formato YYYY-MM-DD
		self.capacidades = capacidades  # dict: {'GRAD': int, 'GRAM': int, 'VIP': int}
		self.precios = precios          # dict: {'GRAD': float, 'GRAM': float, 'VIP': float}
