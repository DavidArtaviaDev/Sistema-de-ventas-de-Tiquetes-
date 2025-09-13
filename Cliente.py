import hashlib

class Cliente:
    def __init__(self, id_cliente, nombre, es_platinum, clave): #el constructor con 4 parametros
        if not id_cliente or not nombre or not clave: #comprueba que los campos no esten vacios 
            raise ValueError("El ID, el nombre y la clave del cliente son obligatorios.")
        self.id_cliente = id_cliente
        self.nombre = nombre
        if isinstance(es_platinum, str):
            es_platinum = es_platinum.strip().lower()  # eliminar espacios y pasar a minúscula
            if es_platinum == "si":
                self.es_platinum = True
            elif es_platinum == "no":
                self.es_platinum = False
            else:
                raise ValueError("es_platinum debe ser 'si' o 'no'.")
        else:
            self.es_platinum = bool(es_platinum)  # si se pasa directamente booleano

        self.hash_clave = hashlib.sha256(clave.encode()).hexdigest() #convierte la clave a sha256

    def verificar_clave(self, clave_intento):
        return self.hash_clave == hashlib.sha256(clave_intento.encode()).hexdigest() #verifica que la clave coincida

    def to_dict(self):
        return { #convierte el objeto cliente a un diccionario para guardarlo en el csv
            "id_cliente": self.id_cliente,
            "nombre": self.nombre,
            "es_platinum": self.es_platinum,
            "hash_clave": self.hash_clave
        }
    def __str__(self):
     return f"{self.id_cliente} - {self.nombre} ({'Platinum' if self.es_platinum else 'Normal'})"



