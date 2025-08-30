# Clase Cliente para el sistema de tiquetera
class Cliente:
	def __init__(self, id_cliente: str, nombre: str, es_platinum: bool, hash_clave: str):
		self.id_cliente = id_cliente  # str: ID único del cliente
		self.nombre = nombre          # str: Nombre del cliente
		self.es_platinum = es_platinum  # bool: Indica si el cliente es platinum
		self.hash_clave = hash_clave    # str: Hash SHA-256 de la clave


