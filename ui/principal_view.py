import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry  # Necesario para los selectores de fecha


class PrincipalView:
    """
    Clase encargada exclusivamente de la construcción y gestión de la interfaz visual.
    Incluye: Búsqueda por rango de fechas, filtrado por estado y coloreado dinámico.
    """

    def __init__(self, root, callbacks):
        """
        Constructor de la vista.
        root: Ventana principal de Tkinter.
        callbacks: Diccionario con las funciones del controlador.
        """
        self.root = root
        self.callbacks = callbacks

        # Ejecuta la construcción de los componentes visuales
        self._construir_interfaz()

        # --- CONFIGURACIÓN DE COLORES (TAGS) ---
        # Estos tags permiten que al insertar datos, el Treeview cambie el formato visual
        # 'completada': Tareas hechas aparecerán grises y tachadas.
        self.tree.tag_configure('completada', foreground='gray', font=('Arial', 10, 'overstrike'))
        # 'pendiente': Tareas activas aparecerán en color azul.
        self.tree.tag_configure('pendiente', foreground='#0d6efd')

        # --- EVENTOS DE RATÓN ---
        # <Button-3> para Windows/Linux, <Button-2> para macOS (clic derecho)
        self.tree.bind("<Button-3>", self._on_right_click)
        self.tree.bind("<Button-2>", self._on_right_click)

    def _construir_interfaz(self):
        """Define la jerarquía de todos los widgets y su disposición en la ventana."""

        # 1. TÍTULO PRINCIPAL
        tk.Label(self.root, text="Gestor de Tareas Pro", font=("Arial", 16, "bold")).pack(pady=10)

        # 2. --- SECCIÓN DE FILTROS Y BÚSQUEDA ---
        # Usamos un LabelFrame para agrupar visualmente las opciones de filtrado
        frame_busqueda = tk.LabelFrame(self.root, text="Panel de Filtros", padx=10, pady=10)
        frame_busqueda.pack(pady=5, padx=20, fill="x")

        # --- Sub-sección: Fechas ---
        tk.Label(frame_busqueda, text="Desde:").pack(side=tk.LEFT, padx=5)
        self.fecha_desde = DateEntry(frame_busqueda, width=11, background='darkblue',
                                     foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
        self.fecha_desde.pack(side=tk.LEFT, padx=5)

        tk.Label(frame_busqueda, text="Hasta:").pack(side=tk.LEFT, padx=5)
        self.fecha_hasta = DateEntry(frame_busqueda, width=11, background='darkblue',
                                     foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
        self.fecha_hasta.pack(side=tk.LEFT, padx=5)

        # --- Sub-sección: Filtrar por Estado ---
        tk.Label(frame_busqueda, text="Estado:").pack(side=tk.LEFT, padx=(15, 5))
        self.combo_estado = ttk.Combobox(
            frame_busqueda,
            values=["Todas", "Pendiente", "Hecho"],
            width=10,
            state="readonly" # Evita que el usuario escriba valores no válidos
        )
        self.combo_estado.current(0)  # Selecciona "Todas" por defecto
        self.combo_estado.pack(side=tk.LEFT, padx=5)

        # --- Botones de Búsqueda ---
        tk.Button(frame_busqueda, text="🔍 Buscar", bg="#e9ecef", font=("Arial", 9, "bold"),
                  command=self.callbacks.get("buscar")).pack(side=tk.LEFT, padx=(15, 5))

        tk.Button(frame_busqueda, text="🔄 Reestablecer", bg="#f8f9fa", font=("Arial", 9),
                  command=self.callbacks.get("reestablecer")).pack(side=tk.LEFT)

        # 3. --- SECCIÓN DE BOTONES DE ACCIÓN ---
        # Botonera superior para gestionar las tareas seleccionadas
        self.frame_botones = tk.Frame(self.root)
        self.frame_botones.pack(pady=10)

        btns = [
            ("➕ Nueva Tarea", self.callbacks["anadir"], "#d4edda"),  # Verde
            ("✏️ Editar", self.callbacks["editar"], "#cfe2ff"),      # Azul
            ("✅ Estado", self.callbacks["alternar"], "#fff3cd"),    # Amarillo
            ("🗑️ Eliminar", self.callbacks["eliminar"], "#f8d7da")    # Rojo
        ]

        for texto, comando, color in btns:
            tk.Button(self.frame_botones, text=texto, command=comando, width=12, bg=color).pack(side=tk.LEFT, padx=5)

        # 4. --- TABLA DE DATOS (Treeview) ---
        self.tree = ttk.Treeview(
            self.root,
            columns=("ID", "Título", "Creado", "Límite", "Estado"),
            show='headings'
        )

        # Configuración de las columnas de la tabla
        columnas = [
            ("ID", 50), ("Título", 250), ("Creado", 110), ("Límite", 110), ("Estado", 90)
        ]

        for col, width in columnas:
            self.tree.heading(col, text=col)
            # El título se alinea a la izquierda para mejor lectura, el resto al centro
            anchor_val = tk.W if col == "Título" else tk.CENTER
            self.tree.column(col, width=width, anchor=anchor_val)

        # Fill y Expand permiten que la tabla crezca con la ventana
        self.tree.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

    def _on_right_click(self, event):
        """
        Detecta el clic derecho, selecciona la fila bajo el cursor
        y lanza el menú contextual a través del callback.
        """
        item_id = self.tree.identify_row(event.y)
        if item_id:
            self.tree.selection_set(item_id)
            if "menu_contextual" in self.callbacks:
                self.callbacks["menu_contextual"](event)

    def obtener_filtros(self):
        """
        Helper para que el controlador pueda leer los valores de los filtros.
        Retorna: (fecha_desde, fecha_hasta, estado_seleccionado)
        """
        return (
            self.fecha_desde.get(),
            self.fecha_hasta.get(),
            self.combo_estado.get()
        )

    def resetear_fechas_filtro(self):
        """
        Limpia solo los selectores de fecha de la búsqueda.
        """
        import datetime
        hoy = datetime.date.today()
        self.fecha_desde.set_date(hoy)
        self.fecha_hasta.set_date(hoy)