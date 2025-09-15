# Clase Evento para el sistema de tiquetera
class Evento:

  def __init__(self, id_evento, nombre, fecha_iso, cap_grad, cap_gram, cap_vip, precio_grad, precio_gram, precio_vip): 
         if not id_evento or not nombre: #verifica que no esten vacios
            raise ValueError("El ID y el nombre del evento son obligatorios.")
         
         if int(cap_grad) < 0 or int(cap_gram) < 0 or int(cap_vip) < 0: #combrueba que no sean negativos
            raise ValueError("Las capacidades deben ser >= 0.")
         if int(precio_grad) < 0 or int(precio_gram) < 0 or int(precio_vip) < 0:
            raise ValueError("Los precios deben ser >= 0.")
         

         for campo, valor in { #recorre el diccionario y comprueba que no sea numero negativo y que sea entero
            "precio gradería": precio_grad,
            "precio gramilla": precio_gram,
            "precio VIP": precio_vip
        }.items():
            if not str(valor).isdigit():
                raise ValueError(f"El {campo} debe ser un número entero.")
            if int(valor) < 0:
                raise ValueError(f"El {campo} no puede ser negativo.")

         self.id_evento = id_evento
         self.nombre = nombre
         self.fecha_iso = fecha_iso
         self.cap_grad = int(cap_grad)
         self.cap_gram = int(cap_gram)
         self.cap_vip = int(cap_vip)
         self.precio_grad = int(precio_grad)
         self.precio_gram = int(precio_gram)
         self.precio_vip = int(precio_vip)


         self.capacidades = { #agrupa capacidades en un diccionario
             "Graderia": int(cap_grad),
            "Gramilla": int(cap_gram),
            "VIP": int(cap_vip)
         }
         self.precios = { # agrupa precios en un diccionario
            "Graderia": int(precio_grad),
            "Gramilla": int(precio_gram),
            "VIP": int(precio_vip)
        }
         
  def to_dict(self):
        # Devuelve un diccionario con todos los valores
        return {
            "id_evento": self.id_evento,
            "nombre": self.nombre,
            "fecha_iso": self.fecha_iso,
            "cap_grad": self.capacidades["Graderia"],
            "cap_gram": self.capacidades["Gramilla"],
            "cap_vip": self.capacidades["VIP"],
            "precio_grad": self.precios["Graderia"],
            "precio_gram": self.precios["Gramilla"],
            "precio_vip": self.precios["VIP"]
        }
  def __str__(self):
        return (f"[{self.id_evento}] {self.nombre} ({self.fecha_iso}) | "
                f"Capacidades: Gradería={self.capacidades['Graderia']}, "
                f"Gramilla={self.capacidades['Gramilla']}, VIP={self.capacidades['VIP']} | "
                f"Precios: Gradería={self.precios['Graderia']}, "
                f"Gramilla={self.precios['Gramilla']}, VIP={self.precios['VIP']}")



