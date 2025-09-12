














































































































import csv

class CSVManager:

    @staticmethod
    def cargar_csv(ruta, fieldnames):
        """Lee un archivo CSV y devuelve una lista de diccionarios."""
        filas = []
        try:
            with open(ruta, mode="r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Validar que tenga todas las columnas esperadas
                    if all(campo in row for campo in fieldnames):
                        filas.append(row)
                    else:
                        print(f"Fila corrupta en {ruta}: {row}")
        except FileNotFoundError:
            print(f"Archivo {ruta} no encontrado. Se creará al guardar.")
        return filas

    @staticmethod
    def guardar_csv(ruta, fieldnames, filas):
        """Escribe una lista de diccionarios en un archivo CSV."""
        with open(ruta, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for fila in filas:
                writer.writerow(fila)
