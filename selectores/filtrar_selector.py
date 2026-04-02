from datetime import datetime

class FiltrarSelector:
    """
    Clase especializada en filtrar colecciones de tareas.
    No toca la base de datos ni la UI, solo recibe una lista y devuelve otra.
    """

    @staticmethod
    def ejecutar(lista_tareas, f_desde_str, f_hasta_str, estado_filtro):
        """
        Filtra una lista de objetos Tarea basándose en criterios de fecha y estado.
        """
        try:
            # Parseo de fechas para comparación lógica
            f_desde = datetime.strptime(f_desde_str, "%d/%m/%Y")
            f_hasta = datetime.strptime(f_hasta_str, "%d/%m/%Y")
        except (ValueError, TypeError):
            # Si las fechas son inválidas, devolvemos la lista sin filtrar para evitar errores
            return lista_tareas

        resultado = []

        for tarea in lista_tareas:
            # 1. Convertir fecha de la tarea
            try:
                t_fecha = datetime.strptime(tarea.fecha_inicio, "%d/%m/%Y")
            except:
                continue # Saltar tareas con fechas corruptas

            # 2. Lógica de Rango
            dentro_de_rango = f_desde <= t_fecha <= f_hasta

            # 3. Lógica de Estado
            cumple_estado = False
            if estado_filtro == "Todas":
                cumple_estado = True
            elif estado_filtro == "Hecho" and tarea.completada:
                cumple_estado = True
            elif estado_filtro == "Pendiente" and not tarea.completada:
                cumple_estado = True

            # Si pasa ambos filtros, se añade al resultado
            if dentro_de_rango and cumple_estado:
                resultado.append(tarea)

        return resultado