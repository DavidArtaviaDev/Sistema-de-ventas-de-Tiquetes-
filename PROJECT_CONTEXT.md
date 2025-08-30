# Contexto y Reglas para el Proyecto Tiquetera de Eventos

## 1. Requerimientos Funcionales Clave (Extracto del PDF)

-**Gestión de Entidades**: El sistema debe permitir crear, editar, eliminar y buscar eventos, así como registrar clientes.

- **Cola de Compras**: Usar una **cola de prioridad** (`heapq`) para gestionar la compra de entradas. Los clientes con `es_platinum = True` tienen preferencia.
- **Simulación de Ingreso**: Usar una **cola de prioridad** para simular el ingreso al evento.
  Los asistentes con tickets del sector `VIP` tienen prioridad. -**Función Deshacer (Undo)**: Usar una **pila** (`list` como stack) para revertir operaciones como compras o cancelaciones.
- **Algoritmos de Ordenamiento**: Se deben implementar **MergeSort** y **QuickSort manualmente** para ordenar la lista de eventos.No se debe usar la función `sorted()` de Python. -**Persistencia de Datos**: Toda la información de eventos, clientes y tickets debe guardarse y cargarse desde **archivos CSV**.
- **Autenticación de Clientes**: Los clientes deben poder iniciar sesión con un ID y una clave. Las contraseñas se almacenan como un **hash SHA-256**.El sistema debe manejar intentos fallidos. -**Validaciones Robustas**: El sistema debe validar todos los datos de entrada, como IDs únicos, formatos de fecha `YYYY-MM-DD`, y la integridad de los archivos CSV.

## 2. Estructura de Clases (Arquitectura UML)

- **`Tiquetera`**: Clase principal que orquesta todo. Contiene las listas de eventos, clientes, tickets, y las estructuras de datos principales (colas y pila). Es el punto de entrada para todas las operaciones.
- **`Evento`**: Almacena datos de un evento (ID, nombre, fecha, capacidades por sector, precios).
- **`Cliente`**: Almacena datos del cliente (ID, nombre, `es_platinum`, `hash_clave`).
- **`Ticket`**: Representa una entrada vendida (ID, evento asociado, cliente asociado, sector, estado).
- **`Auth`**: Maneja la lógica de registro y autenticación de clientes, incluyendo el control de intentos fallidos y bloqueos.
- **`SolicitudCompra`**: Objeto que se encola en la `cola_compras`. Contiene los datos de una solicitud de compra y calcula su propia prioridad.
- **`Operacion`**: Objeto que se apila en `operaciones_deshacer`. Contiene la información necesaria para revertir una acción.
- **`Config`**: Clase estática para centralizar constantes (nombres de sectores, rutas de archivos, estados de tickets, etc.).
- **`CSVManager`**: Clase estática responsable de toda la lógica de lectura y escritura de archivos CSV, incluyendo la validación de esquemas.
- **`Logger`**: Clase estática para manejar el registro de errores, operaciones y accesos.

## 3. Formato Esperado de Archivos CSV

-**`eventos.csv`**: `id_evento,nombre,fecha_iso,cap_grad,cap_gram,cap_vip,precio_grad,precio_gram,precio_vip` -**`clientes.csv`**: `id_cliente,nombre,es_platinum,hash_clave` -**`tickets.csv`**: `id_ticket,id_evento,id_cliente,sector,precio,estado,fecha_compra`
