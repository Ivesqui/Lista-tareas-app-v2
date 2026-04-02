class AyudaServicio:
    """
    Servicio encargado de la persistencia y gestión de los atajos de teclado.
    Actúa como la Fuente de Verdad para saber qué teclas disparan qué acciones.
    """

    def __init__(self):
        """
        Inicializa el diccionario de atajos por defecto.
        En una versión más avanzada, estos datos podrían cargarse desde un archivo JSON o SQLite.
        """
        # El diccionario utiliza nombres de acciones como llaves y 
        # el formato de cadena de Tkinter para las teclas como valores.
        self.atajos = {
            "eliminar": "Delete",  # Tecla simple (suprimir)
            "completar": "c",  # tecla c
            "editar": "e",  # tecla e
            "ayuda": "F1",  # Tecla de función estándar para manuales
            "salir": "Escape"  # Tecla para cerrar ventanas o cancelar
        }

    def obtener_atajos(self):
        """
        Retorna el diccionario completo de atajos actuales.
        Útil para el ShortcutsDialog al generar la interfaz de configuración.
        """
        return self.atajos

    def actualizar_atajo(self, accion, nueva_tecla):
        """
        Modifica un atajo de teclado específico en el diccionario.

        accion: La llave del diccionario (ej: 'eliminar').
        nueva_tecla: La cadena que representa la nueva tecla (ej: 'Control-d').
        """
        # Normalización: Tkinter prefiere los guiones '-' para separar combinaciones.
        # Si el usuario escribe 'Control+k', lo convertimos automáticamente a 'Control-k'.
        self.atajos[accion] = nueva_tecla.replace("+", "-")

        # Nota: En este punto se podría añadir una línea para guardar en un archivo 
        # y que los cambios no se pierdan al cerrar el programa.