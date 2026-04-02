import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
from ui.menu_bar import AppMenu  # Clase encargada de la lógica de menús


class TareaForm:
    """Ventana emergente para crear o editar tareas."""

    def __init__(self, parent, callback_guardar, tarea_a_editar=None):
        """
        Constructor del formulario.
        parent: ventana principal que lanza el formulario.
        callback_guardar: función que procesará los datos al guardar.
        tarea_a_editar: objeto tarea (opcional) para cargar datos existentes.
        """
        self.top = tk.Toplevel(parent)
        self.callback_guardar = callback_guardar
        self.tarea_a_editar = tarea_a_editar

        # --- Configuración de la ventana ---
        self.top.title("Editar Tarea" if self.tarea_a_editar else "Nueva Tarea")
        self.top.geometry("550x450")

        # Bloquea la interacción con la ventana principal hasta que esta se cierre
        self.top.grab_set()

        # --- CONFIGURACIÓN DEL MENÚ ---
        # 1. Creamos una instancia de Menu para el Toplevel
        self.barra_tarea = tk.Menu(self.top)

        # 2. Inyectamos solo el menú de Edición usando el método estático de AppMenu.
        # Guardamos la función de retorno para usarla en atajos de teclado si fuera necesario.
        self.lanzar_comando = AppMenu._menu_edicion(self.barra_tarea, self.top)

        # 3. Asignamos la barra de menú configurada a la ventana Toplevel
        self.top.config(menu=self.barra_tarea)

        # --- INTERFAZ Y DATOS ---
        # Llamamos a la construcción de los widgets visuales
        self._construir_interfaz()

        # Si recibimos una tarea para editar, rellenamos los campos automáticamente
        if self.tarea_a_editar:
            self._cargar_datos_existentes()

        # --- ATAJOS DE TECLADO ---
        # Permite guardar la tarea rápidamente presionando la tecla Enter
        self.top.bind("<Return>", lambda e: self._enviar_datos())

    def _construir_interfaz(self):
        """Crea todos los widgets visuales del formulario."""

        # --- Campo: Título ---
        tk.Label(self.top, text="Título de la Tarea:", font=("Arial", 10, "bold")).pack(pady=5)

        # Usamos tk.Entry para el título. No incluimos 'undo=True' porque causa error
        # en muchas versiones de Tkinter para este widget específico.
        self.ent_titulo = tk.Entry(self.top, width=40, font=("Arial", 10))
        self.ent_titulo.pack(pady=5)

        # Ponemos el foco inicial en el título para que el usuario empiece a escribir de inmediato
        self.ent_titulo.focus_set()

        # --- Campo: Descripción Extendida ---
        # Variable de control para saber si el cuadro de texto debe estar activo o no
        self.check_var = tk.BooleanVar(value=True)
        tk.Checkbutton(self.top, text="Agregar descripción extendida",
                       variable=self.check_var, command=self._toggle_desc).pack(pady=5)

        # tk.Text sí soporta 'undo=True', permitiendo el historial de Deshacer/Rehacer
        self.txt_desc = tk.Text(self.top, width=40, height=5, font=("Arial", 10), undo=True)
        self.txt_desc.pack(pady=5)

        # --- Contenedor: Rango de Fechas ---
        # Usamos un LabelFrame para agrupar visualmente los selectores de fecha
        frame_fechas = tk.LabelFrame(self.top, text="Rango de Ejecución", padx=10, pady=10)
        frame_fechas.pack(pady=15)

        # Fecha de Inicio
        tk.Label(frame_fechas, text="Desde:").grid(row=0, column=0, sticky="w")
        self.cal_inicio = DateEntry(frame_fechas, width=12, background='darkblue',
                                    foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
        self.cal_inicio.grid(row=0, column=1, padx=5, pady=5)

        # Fecha de Fin
        tk.Label(frame_fechas, text="Hasta:").grid(row=1, column=0, sticky="w")
        self.cal_fin = DateEntry(frame_fechas, width=12, background='darkblue',
                                 foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
        self.cal_fin.grid(row=1, column=1, padx=5, pady=5)

        # --- Botones de Acción ---
        # Definimos texto y color dinámicamente según si editamos o creamos
        texto_boton = "Actualizar Cambios" if self.tarea_a_editar else "Guardar Tarea"
        color_boton = "#cfe2ff" if self.tarea_a_editar else "#d4edda"

        self.btn_guardar = tk.Button(self.top, text=texto_boton, bg=color_boton,
                                     font=("Arial", 10, "bold"), width=20,
                                     command=self._enviar_datos)
        self.btn_guardar.pack(pady=20)

        # Botón para cerrar la ventana sin guardar nada
        tk.Button(self.top, text="Cancelar", command=self.top.destroy,
                  width=20, bg="#f8d7da").pack()

    def _cargar_datos_existentes(self):
        """Rellena los campos con la información de la tarea recibida."""
        # Insertamos el título
        self.ent_titulo.insert(0, self.tarea_a_editar.titulo)

        # Limpiamos e insertamos la descripción
        self.txt_desc.delete("1.0", tk.END)
        if self.tarea_a_editar.descripcion and self.tarea_a_editar.descripcion != "(No se ha agregado una descripción)":
            self.txt_desc.insert("1.0", self.tarea_a_editar.descripcion)
            # IMPORTANTE: Reiniciamos el historial de edición para que el 'Deshacer'
            # no borre la carga inicial de datos.
            self.txt_desc.edit_reset()
        else:
            # Si no hay descripción, desactivamos el checkbox y el campo
            self.check_var.set(False)
            self._toggle_desc()

        # Ajustamos las fechas en los calendarios
        self.cal_inicio.set_date(self.tarea_a_editar.fecha_inicio)
        self.cal_fin.set_date(self.tarea_a_editar.fecha_fin)

    def _toggle_desc(self):
        """Habilita o deshabilita el campo de descripción según el checkbox."""
        if self.check_var.get():
            self.txt_desc.config(state=tk.NORMAL, bg="white")
        else:
            # Si se deshabilita, limpiamos el texto y cambiamos el color de fondo
            self.txt_desc.delete("1.0", tk.END)
            self.txt_desc.config(state=tk.DISABLED, bg="#f0f0f0")

    def _enviar_datos(self):
        """Valida los campos y envía la información al controlador mediante el callback."""
        titulo = self.ent_titulo.get().strip()
        # Obtenemos el texto de la descripción eliminando el salto de línea final automático
        desc = self.txt_desc.get("1.0", "end-1c").strip() if self.check_var.get() else ""
        f_ini = self.cal_inicio.get()
        f_fin = self.cal_fin.get()

        # Validación simple de campo obligatorio
        if not titulo:
            messagebox.showwarning("Faltan datos", "El título es obligatorio.")
            return

        # CAPTURAMOS EL RESULTADO DEL CONTROLADOR
        exito = self.callback_guardar(titulo, desc, f_ini, f_fin)

        # SOLO SI ES TRUE, CERRAMOS LA VENTANA
        if exito:
            self.top.destroy()
        # Si es False (porque hubo error de fechas), no hacemos nada y la ventana sigue abierta.