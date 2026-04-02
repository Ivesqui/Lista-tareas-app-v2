import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
from ui.principal_view import PrincipalView
from ui.menu_bar import AppMenu
from ui.tarea_form import TareaForm
from controladores.ayuda_controlador import AyudaController
from selectores.filtrar_selector import FiltrarSelector


class TareaController:
    """
    Controlador Maestro de la aplicación.
    Coordina la interacción entre la interfaz de usuario, la lógica de negocio
    y los controladores auxiliares.
    """
    def __init__(self, root, servicio, config_servicio):
        """
        root: Ventana principal de Tkinter.
        servicio: Instancia de TareaServicio (Lógica de datos).
        config_servicio: Instancia de AyudaServicio (Lógica de configuración/atajos).
        """
        self.root = root
        self.servicio = servicio
        self.config_servicio = config_servicio

        # 1. DEFINICIÓN DE CALLBACKS
        # Diccionario de funciones que le pasamos a la Vista.
        # Cuando el usuario pulsa un botón en la interfaz, la Vista ejecuta estas funciones.
        callbacks = {
            "anadir": self.abrir_formulario_nueva_tarea,
            "buscar": self.buscar_segun_parametros,
            "reestablecer": self.reestablecer_filtros,
            "editar": self.editar_seleccionada,
            "alternar": self.alternar_seleccionada,
            "eliminar": self.eliminar_seleccionada,
            "menu_contextual": self.mostrar_menu_contextual
        }

        # 2. INICIALIZACIÓN DE LA VISTA
        # Creamos la interfaz pasando los callbacks anteriores.
        self.view = PrincipalView(self.root, callbacks)

        # 3. CONTROLADORES AUXILIARES
        # Delegamos la gestión de atajos y menús a clases especializadas.
        self.config_manager = AyudaController(self)
        self.menu_superior = AppMenu(self)

        # 4. CONFIGURACIÓN DE ESTILOS VISUALES (Tags)
        # Creamos una etiqueta llamada 'completada'. Cualquier fila con esta etiqueta
        # se verá gris y con el texto tachado (overstrike).
        self.view.tree.tag_configure('completada', foreground='gray', font=('Arial', 10, 'overstrike'))

        # 5. ARRANQUE DEL SISTEMA
        # Vinculamos las teclas configuradas y cargamos las tareas existentes en la tabla.
        self.config_manager.vincular_atajos()
        self.actualizar_lista()

    # --- GESTIÓN DE FORMULARIOS (Alta y Edición) ---

    def abrir_formulario_nueva_tarea(self):
        """Lanza la ventana emergente para registrar una tarea desde cero."""
        TareaForm(self.root, self.guardar_nueva_tarea)

    def guardar_nueva_tarea(self, titulo, desc, f_ini, f_fin):
        """Procesa los datos del formulario y registra una nueva tarea."""

        if not titulo.strip():
            messagebox.showwarning("Error", "El título es obligatorio.")
            return

        # Validamos las fechas
        valido, error, _, _ = self._validar_rango_fechas(f_ini, f_fin)

        if not valido:
            if error == "RANGO_INVALIDO":
                messagebox.showwarning(
                    "Rango Inválido",
                    "La fecha de inicio no puede ser mayor a la de fin."
                )
                # El usuario debe corregir el formulario, no queremos tocar la búsqueda principal todavía.

            elif error == "FORMATO_INVALIDO":
                messagebox.showerror(
                    "Error de Formato",
                    "Las fechas no tienen un formato válido (dd/mm/yyyy)."
                )
            return False # Se detiene aquí, el formulario sigue abierto.

        # Si todo esta bien guardamos
        self.servicio.agregar_tarea(titulo, desc, f_ini, f_fin)

        # REFRESCAMOS
        self.actualizar_lista()
        self._refrescar_calendario_si_existe()

        # Retornamos True para avisarle al formulario que ya puede cerrarse
        return True

    def editar_seleccionada(self):
        """Detecta qué tarea está marcada en la tabla y abre el formulario para modificarla."""
        id_t = self._obtener_id()
        if id_t:
            # Buscamos el objeto tarea real en el servicio usando su ID
            tarea = next((t for t in self.servicio.obtener_todas() if t.id == id_t), None)

            if tarea:
                # Abrimos el mismo formulario, pero inyectando los datos de la tarea elegida
                TareaForm(self.root, self.guardar_edicion_tarea, tarea_a_editar=tarea)

    def guardar_edicion_tarea(self, titulo, desc, fecha_ini, fecha_fin):
        """Aplica los cambios realizados en el formulario de edición a una tarea existente."""

        id_t = self._obtener_id()
        if not id_t:
            return False

        if not titulo.strip():
            messagebox.showwarning("Error", "El título es obligatorio.")
            return

        # Usamos el validador centralizado (le pasamos los STRINGS directamente)
        valido, error,_, _ = self._validar_rango_fechas(fecha_ini, fecha_fin)

        if not valido:
            if error == "RANGO_INVALIDO":
                messagebox.showwarning(
                    "Rango Inválido",
                    "La fecha de inicio no puede ser mayor a la de fin."
                )
                # El usuario debe corregir el formulario, no queremos tocar la búsqueda principal todavía.

            elif error == "FORMATO_INVALIDO":
                messagebox.showerror(
                    "Error de Formato",
                    "Las fechas no tienen un formato válido (dd/mm/yyyy)."
                )
            return False # Se detiene aquí, el formulario sigue abierto.

        # Si es válido, guardamos cambios directamente con los strings originales
        self.servicio.actualizar_tarea_completa(id_t, titulo, desc, fecha_ini, fecha_fin)

        # Refrescar UI
        self.actualizar_lista()
        self._refrescar_calendario_si_existe()
        # Retornamos True para avisarle al formulario que ya puede cerrarse
        return True

    # --- LÓGICA DE ESTADO Y ELIMINACIÓN ---

    def alternar_seleccionada(self):
        """Pasa una tarea de 'Pendiente' a 'Hecho' o viceversa."""
        id_t = self._obtener_id()
        if id_t:
            self.servicio.alternar_estado_tarea(id_t)
            self.actualizar_lista()
            self._refrescar_calendario_si_existe()

    def eliminar_seleccionada(self):
        """Borra definitivamente la tarea tras una confirmación de seguridad."""
        id_t = self._obtener_id()
        if id_t and messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar esta tarea?"):
            self.servicio.eliminar_tarea(id_t)
            self.actualizar_lista()
            self._refrescar_calendario_si_existe()

    # --- ACTUALIZACIÓN E INTERACCIONES DE INTERFAZ (LISTA TTK) ---

    def actualizar_lista(self):
        """
        Sincroniza la tabla visual (Treeview) con la lista de tareas del Servicio.
        """
        # 1. Vaciamos la tabla actual
        for i in self.view.tree.get_children():
            self.view.tree.delete(i)

        # 2. Obtenemos las tareas del servicio y las insertamos una por una
        for t in self.servicio.obtener_todas():
            estado = "✅ Hecho" if t.completada else "⏳ Pendiente"
            # Aplicamos el tag 'completada' si corresponde para el efecto visual de tachado
            tag = ('completada',) if t.completada else ()

            self.view.tree.insert("", tk.END,
                                  values=(t.id, t.titulo, t.fecha_inicio, t.fecha_fin, estado),
                                  tags=tag)

    def buscar_segun_parametros(self):
        """Manejador del botón buscar que utiliza el Validador y el Selector."""

        # Obtener datos de la UI
        f_ini_str, f_fin_str, estado = self.view.obtener_filtros()

        # Validamos el rango de fechas
        valido, error, _, _ = self._validar_rango_fechas(f_ini_str, f_fin_str)

        if not valido:
            if error == "RANGO_INVALIDO":
                messagebox.showwarning(
                    "Rango de Búsqueda Inválido",
                    "La fecha 'Desde' no puede ser mayor que 'Hasta'."
                )
                # Reestablecemos los DateEntry de la búsqueda para ayudar al usuario
                self.view.resetear_fechas_filtro()

            elif error == "FORMATO_INVALIDO":
                messagebox.showerror(
                    "Error",
                    "El formato de fecha de búsqueda no es correcto."
                )
            return

        # Si pasa la validación, obtenemos datos y filtramos
        tareas = self.servicio.obtener_todas()

        # Usamos el Selector
        filtradas = FiltrarSelector.ejecutar(
            tareas, f_ini_str, f_fin_str, estado
        )
        # Refrescar la tabla con el resultado
        self._rellenar_tabla(filtradas)

    def _rellenar_tabla(self, lista):
        self.view.tree.delete(*self.view.tree.get_children())
        for t in lista:
            estado_txt = "✅ Hecho" if t.completada else "⏳ Pendiente"
            # USAR LOS TAGS AQUÍ PARA LOS COLORES
            tag = 'completada' if t.completada else 'pendiente'

            self.view.tree.insert("", "end",
                                  values=(t.id, t.titulo, t.fecha_inicio, t.fecha_fin, estado_txt),
                                  tags=(tag,))

    def reestablecer_filtros(self):
        # Resetear UI
        self.view.combo_estado.set("Todas")

        # Opcional: resetear fechas a hoy
        from datetime import datetime
        hoy = datetime.now().strftime("%d/%m/%Y")

        self.view.fecha_desde.set_date(hoy)
        self.view.fecha_hasta.set_date(hoy)

        # Recargar todas las tareas
        tareas = self.servicio.obtener_todas()
        self._rellenar_tabla(tareas)


    def actualizar_calendario_grande(self, calendario_widget):
        """
        Dibuja marcas de eventos en el widget de calendario para tareas pendientes.
        """
        if not calendario_widget:
            return

        # Limpiamos marcas anteriores
        calendario_widget.calevent_remove('all')


        for t in self.servicio.obtener_todas():
            # Solo mostramos en el calendario lo que aún no se ha terminado
            if not t.completada:
                try:
                    # Convertimos las fechas de texto (dd/mm/yyyy) a objetos datetime
                    inicio = datetime.strptime(t.fecha_inicio, "%d/%m/%Y")
                    fin = datetime.strptime(t.fecha_fin, "%d/%m/%Y")

                    # Marcamos cada día del rango en el calendario
                    actual = inicio

                    while actual <= fin:
                        calendario_widget.calevent_create(actual, t.titulo, 'pendiente')
                        actual += timedelta(days=1)
                except (ValueError, TypeError):
                    # Si hay un error de formato de fecha, saltamos esta tarea
                    continue

        # Estilo de las marcas: azul con letras blancas
        calendario_widget.tag_config('pendiente', background='blue', foreground='white')

    def _refrescar_calendario_si_existe(self):
        """Verifica si la vista tiene un calendario activo antes de intentar actualizarlo."""
        if hasattr(self.view, 'calendario_widget'):
            self.actualizar_calendario_grande(self.view.calendario_widget)

    # --- MENÚ CONTEXTUAL Y DETALLES ---

    def mostrar_menu_contextual(self, event):
        """Crea y despliega un menú flotante al hacer clic derecho sobre una fila."""
        # Identificamos la fila bajo el cursor
        item = self.view.tree.identify_row(event.y)
        if item:
            # Seleccionamos visualmente la fila
            self.view.tree.selection_set(item)

            # Creamos el menú flotante
            menu = tk.Menu(self.root, tearoff=0)
            menu.add_command(label="🔍 Ver Detalles Completo", command=self.abrir_ventana_detalles)
            menu.add_separator()
            menu.add_command(label="✅ Alternar Estado", command=self.alternar_seleccionada)
            menu.add_command(label="❌ Eliminar", command=self.eliminar_seleccionada)

            # Lanzamos el menú en la posición del ratón
            try:
                menu.tk_popup(event.x_root, event.y_root)
            finally:
                # Liberamos el foco del menú al cerrar
                menu.grab_release()

    def abrir_ventana_detalles(self):
        """Instancia la vista de detalles para mostrar la descripción extendida."""
        id_t = self._obtener_id()
        if not id_t:
            return

        tarea = next((t for t in self.servicio.obtener_todas() if t.id == id_t), None)

        if tarea:
            from ui.detalle_view import DetalleView
            DetalleView(self.root, tarea)

    # --- HELPERS DE SOPORTE ---

    def _obtener_id(self):
        """
        Extrae el valor de la columna ID de la tarea seleccionada en el Treeview.
        Retorna el ID (int) o None si no hay selección.
        """
        sel = self.view.tree.selection()
        if not sel:
            messagebox.showinfo("Selección", "Por favor, selecciona una tarea de la lista.")
            return None
        # Accedemos a la tupla de valores de la fila y tomamos el primero (índice 0)
        return self.view.tree.item(sel)['values'][0]

    def _validar_rango_fechas(self, f_ini_str, f_fin_str):
        try:
            f_ini = datetime.strptime(f_ini_str, "%d/%m/%Y")
            f_fin = datetime.strptime(f_fin_str, "%d/%m/%Y")

            if f_ini > f_fin:
                return False, "RANGO_INVALIDO", None, None

            return True, None, f_ini, f_fin

        except (ValueError, TypeError):
            return False, "FORMATO_INVALIDO", None, None