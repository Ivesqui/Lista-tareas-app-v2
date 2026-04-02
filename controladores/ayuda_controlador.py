import webbrowser
from ui.atajos_dialog import AtajosDialog


class AyudaController:
    """
    Controlador encargado de la gestión de ayuda y la configuración dinámica
    de los atajos de teclado (Key Bindings).
    """

    def __init__(self, app_instance):
        """
        Constructor del controlador de ayuda.
        app_instance: Referencia al controlador principal (TareaController)
        para acceder a la vista y a los servicios.
        """
        self.app = app_instance

    def vincular_atajos(self):
        """
        Método central que configura el teclado.
        Lee las preferencias del servicio y las aplica físicamente a la ventana.
        """
        # 1. Obtenemos el diccionario de atajos actual (ej: {'editar': 'Control-e'})
        atajos = self.app.config_servicio.obtener_atajos()

        # 2. Mapeamos los nombres de las acciones con los métodos reales del controlador principal
        mapeo_acciones = {
            "salir": self.app.root.quit,
            "eliminar": self.app.eliminar_seleccionada,
            "completar": self.app.alternar_seleccionada,
            "editar": self.app.editar_seleccionada,
            "ayuda": self.abrir_github
        }

        # 3. Limpiamos todos los binds previos para evitar duplicados o conflictos
        # al reconfigurar las teclas.
        self.app.root.unbind_all("<Key>")

        # 4. Iteramos sobre los atajos para realizar el registro (bind) en Tkinter
        for nombre_accion, tecla in atajos.items():
            if nombre_accion in mapeo_acciones:
                func = mapeo_acciones[nombre_accion]

                # Limpiamos los caracteres '<' y '>' si el usuario los escribió,
                # ya que los añadiremos de forma estandarizada.
                t = tecla.strip("<>")

                # --- Lógica de Binds según el tipo de tecla ---

                # Caso A: Combinaciones (ej: "Control-k")
                if "-" in t:
                    # Usamos un parámetro por defecto (f=func) en la lambda para
                    # "congelar" la función correcta en cada iteración del ciclo.
                    self.app.root.bind(f"<{t}>", lambda e, f=func: f())

                # Caso B: Teclas de una sola letra (ej: "e")
                elif len(t) == 1:
                    # Registramos tanto en minúscula como en mayúscula para que
                    # funcione sin importar el estado de Bloq Mayús.
                    self.app.root.bind(f"<{t.lower()}>", lambda e, f=func: f())
                    self.app.root.bind(f"<{t.upper()}>", lambda e, f=func: f())

                # Caso C: Teclas especiales o de función (ej: "F1", "Delete", "Escape")
                else:
                    self.app.root.bind(f"<{t}>", lambda e, f=func: f())

        # --- Binds fijos de los widgets ---
        # El doble clic en el Treeview siempre alternará el estado (completado/pendiente)
        self.app.view.tree.bind("<Double-1>", lambda e: self.app.alternar_seleccionada())

    def ventana_config_atajos(self):
        """Abre el cuadro de diálogo para que el usuario personalice sus teclas."""
        AtajosDialog(self.app)

    def abrir_github(self):
        """Abre el repositorio del proyecto en el navegador web predeterminado."""
        webbrowser.open("https://github.com/ivesqui/Lista-tareas-app-v2")