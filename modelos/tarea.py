class Tarea:
    """
    Clase que representa la entidad 'Tarea'.
    Define la estructura de datos y el comportamiento básico de cada tarea individual.
    """

    def __init__(self, id_tarea, titulo, descripcion, fecha_inicio, fecha_fin, completada=False):
        """
        Constructor de la clase Tarea.

        id_tarea: Identificador único (ID) asignado por el servicio.
        titulo: Nombre o resumen de la tarea.
        descripcion: Texto detallado sobre la actividad.
        fecha_inicio: Fecha programada para comenzar.
        fecha_fin: Fecha límite para terminar.
        completada: Estado de la tarea (por defecto es False/Pendiente).
        """
        self.id = id_tarea
        self.titulo = titulo

        # Validación interna: Si la descripción está vacía o solo tiene espacios,
        # asignamos un texto genérico para evitar campos vacíos en la interfaz.
        self.descripcion = descripcion if descripcion.strip() else "(No se ha agregado una descripción)"

        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.completada = completada

    def cambiar_estado(self):
        """
        Metodo de comportamiento: Invierte el estado actual de la tarea.
        Si estaba pendiente (False), pasa a completada (True) y viceversa.
        """
        self.completada = not self.completada

    def editar_tarea_completa(self, nueva_desc, nueva_fecha):
        """
        Metodo para actualizar campos específicos de la tarea.
        Nota: En tu versión de TareaServicio, este método suele ser reemplazado
        por la asignación directa de atributos, pero es útil para encapsular cambios.
        """
        self.descripcion = nueva_desc
        self.fecha_limite = nueva_fecha  # Nota: Asegúrate de que coincida con 'fecha_fin' si cambias el nombre