class Config: #funciona como contenedor de configuraciones globales
    SECTORES = ["Graderia","Gramilla","VIP"]
    ESTADOS_TICKET = ["emitido"]
    
    
    #atributos de clase que almacena el nombre del archivo CSV donde se guardan los eventos, tickets y clientes 
    ARCHIVO_TICKETS = "tickets.csv"
    ARCHIVO_EVENTOS = "eventos.csv"
    ARCHIVO_CLIENTES = "clientes.csv"
