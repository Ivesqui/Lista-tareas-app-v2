from modelos.tarea import Tarea


class TareaServicio:
    """
    Clase de servicio encargada de la lógica de negocio para las tareas.
    Gestiona el almacenamiento en memoria, la creación, edición y eliminación.
    """

    def __init__(self):
        """
        Inicializa el contenedor de datos.
        _tareas: Lista privada que almacena los objetos de la clase Tarea.
        _contador_id: Generador de IDs únicos para asegurar que cada tarea sea identificable.
        """
        self._tareas = []
        self._contador_id = 1

    def agregar_tarea(self, titulo, descripcion, fecha_inicio, fecha_fin):
        """
        Crea un nuevo objeto Tarea y lo guarda en la lista.

        titulo: Nombre de la actividad.
        descripcion: Detalle de la tarea.
        fecha_inicio / fecha_fin: Fechas de ejecución (objetos date o strings).
        Retorna: El objeto Tarea recién creado.
        """
        # Normalizamos la descripción: si solo hay espacios o está vacía, ponemos un texto por defecto
        desc_limpia = descripcion.strip() if descripcion.strip() else "(Sin descripción)"

        # Instanciamos el modelo Tarea con el ID actual del contador
        nueva_tarea = Tarea(
            id_tarea=self._contador_id,
            titulo=titulo.strip(),
            descripcion=desc_limpia,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )

        # Guardamos en la lista "base de datos" en memoria
        self._tareas.append(nueva_tarea)

        # Incrementamos el contador para la siguiente tarea
        self._contador_id += 1
        return nueva_tarea

    def obtener_todas(self):
        """
        Retorna la lista completa de objetos Tarea.
        Utilizado por el controlador para refrescar la vista (Treeview).
        """
        return self._tareas

    def eliminar_tarea(self, id_tarea):
        """
        Elimina una tarea de la lista mediante una técnica de filtrado.

        id_tarea: El identificador único de la tarea a remover.
        """
        # Reconstruimos la lista excluyendo la tarea que coincida con el ID proporcionado
        self._tareas = [t for t in self._tareas if t.id != id_tarea]

    def alternar_estado_tarea(self, id_tarea):
        """
        Busca una tarea por ID y cambia su estado de Pendiente a Completada (y viceversa).
        """
        for tarea in self._tareas:
            if tarea.id == id_tarea:
                # Invocamos el método de comportamiento definido en el modelo Tarea
                tarea.cambiar_estado()
                break

    def actualizar_tarea_completa(self, id_t, titulo, descripcion, f_inicio, f_fin):
        """
        Busca una tarea existente y actualiza todos sus atributos.

        id_t: ID de la tarea a modificar.
        Retorna: True si la operación fue exitosa, False si no se encontró el ID.
        """
        # Buscamos el objeto tarea dentro de la lista.
        # next() devuelve el primer elemento que cumpla la condición, o None si no hay coincidencias.
        tarea = next((t for t in self._tareas if t.id == id_t), None)

        if tarea:
            # Actualizamos los atributos del objeto encontrado
            tarea.titulo = titulo.strip()

            # Validación rápida para asegurar que la descripción no quede vacía visualmente
            tarea.descripcion = descripcion.strip() if descripcion.strip() else "(Sin descripción)"

            tarea.fecha_inicio = f_inicio
            tarea.fecha_fin = f_fin

            # En una arquitectura con persistencia (Base de Datos), aquí se ejecutaría el COMMIT/SAVE.
            return True

        return False