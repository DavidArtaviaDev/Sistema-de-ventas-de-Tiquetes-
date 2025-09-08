import csv
from Ticket import Ticket

class GestorTickets:
    def __init__(self, archivo="tickets.csv"):
        self.archivo = archivo
        self.tickets = []
        self.cargar_csv()
        
        
     
    def cargar_csv(self):
     pass