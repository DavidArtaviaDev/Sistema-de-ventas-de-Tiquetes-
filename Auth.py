import hashlib

class Auth:
    def __init__(self, lista_clientes):
        self.clientes = lista_clientes
        self.intentos_fallidos = {}
        self.MAX_INTENTOS = 3

    def _hash_clave(self, clave):
        sha256 = hashlib.sha256()
        sha256.update(clave.encode('utf-8'))
        return sha256.hexdigest()

    def autenticar(self, id_cliente, clave):
        """
        Valida las credenciales de un cliente y devuelve un estado y el objeto cliente.

        Args:
            id_cliente (str): El ID del cliente.
            clave (str): La contraseña en texto plano.

        Returns:
            tuple: Una tupla con (str_resultado, objeto_cliente).
                   Posibles resultados: "EXITO", "CLAVE_INCORRECTA", "CLIENTE_NO_ENCONTRADO", "CUENTA_BLOQUEADA".
                   El objeto_cliente es el cliente si el resultado es "EXITO", de lo contrario es None.
        """
        # 1. Verificar si el cliente está bloqueado
        if self.intentos_fallidos.get(id_cliente, 0) >= self.MAX_INTENTOS:
            return "CUENTA_BLOQUEADA", None

        # 2. Buscar al cliente
        cliente_encontrado = next((c for c in self.clientes if c.id_cliente == id_cliente), None)

        if not cliente_encontrado:
            return "CLIENTE_NO_ENCONTRADO", None

        # 3. Hashear y comparar claves
        hash_clave_ingresada = self._hash_clave(clave)

        if hash_clave_ingresada == cliente_encontrado.hash_clave:
            # Éxito: reiniciar intentos y devolver el cliente
            self.intentos_fallidos[id_cliente] = 0
            return "EXITO", cliente_encontrado
        else:
            # Fallo: incrementar intentos y devolver error
            self.intentos_fallidos[id_cliente] = self.intentos_fallidos.get(id_cliente, 0) + 1
            if self.intentos_fallidos.get(id_cliente, 0) >= self.MAX_INTENTOS:
                return "CUENTA_BLOQUEADA", None
            return "CLAVE_INCORRECTA", None 
        