import tkinter as tk
from tkinter import messagebox


class AppMenu:
    """
    Clase encargada de gestionar la barra de menús de la aplicación principal
    y de proporcionar menús contextuales o adicionales para ventanas secundarias.
    """

    def __init__(self, app_instancia):
        """
        Constructor del menú principal.
        app_instancia: Referencia al controlador principal de la aplicación.
        """
        self.app = app_instancia
        self.root = app_instancia.root

        # Creamos la barra de menú principal vinculada a la raíz
        self.barra_menu = tk.Menu(self.root)

        # Construimos las categorías del menú
        self._menu_principal()

    def _menu_principal(self):
        """
        Define y organiza las cascadas (secciones) de la barra de menú principal.
        """
        # --- Menú Aplicación ---
        # tearoff=0 evita que el menú se pueda desprender en una ventana flotante
        menu_app = tk.Menu(self.barra_menu, tearoff=0)
        # Comando para cerrar la aplicación completamente
        menu_app.add_command(label="Salir", command=self.root.quit)
        # Añade "Aplicación" a la barra superior
        self.barra_menu.add_cascade(label="Aplicación", menu=menu_app)

        # --- Menú Ventana ---
        menu_ventana = tk.Menu(self.barra_menu, tearoff=0)
        # Comando para minimizar la ventana principal a la barra de tareas
        menu_ventana.add_command(label="Minimizar", command=self.root.iconify)
        self.barra_menu.add_cascade(label="Ventana", menu=menu_ventana)

        # --- Menú Ayuda ---
        menu_ayuda = tk.Menu(self.barra_menu, tearoff=0)

        # Redirigimos la acción al config_manager para abrir el repositorio o documentación
        menu_ayuda.add_command(
            label="Ayuda (F1)",
            command=self.app.config_manager.abrir_github
        )
        # Abre la ventana de personalización de atajos de teclado
        menu_ayuda.add_command(
            label="Configurar Atajos",
            command=self.app.config_manager.ventana_config_atajos
        )

        # Separador visual entre opciones de configuración y créditos
        menu_ayuda.add_separator()

        # Muestra un cuadro de diálogo con información del autor y versión
        menu_ayuda.add_command(
            label="Acerca de",
            command=lambda: messagebox.showinfo(
                "Acerca de",
                "Gestor de Tareas v2.0 \n by Chris Estupiñan"
            )
        )
        self.barra_menu.add_cascade(label="Ayuda", menu=menu_ayuda)

        # Finalmente, asignamos esta configuración de menú a la ventana root
        self.root.config(menu=self.barra_menu)

    def _lanzar_evento(self, evento):
        """
        Lógica genérica para disparar eventos en el widget que tenga el foco actual.
        Utilizado principalmente para acciones de teclado o botones genéricos.
        """
        # Detectamos qué componente (Entry, Text, etc.) tiene el cursor
        widget = self.root.focus_get()
        if widget:
            try:
                # Generamos el evento (ej: <<Copy>>, <<Paste>>) en dicho widget
                widget.event_generate(evento)
            except tk.TclError:
                # Si el widget no es compatible con la acción, ignoramos el error
                pass

    @staticmethod
    def _menu_edicion(barra_padre, ventana_objetivo):
        """
        Metodo estático para inyectar un menú de 'Edición' en cualquier barra de menú.
        Útil para formularios secundarios (como TareaForm).

        barra_padre: El objeto tk.Menu donde se insertará la cascada.
        ventana_objetivo: La ventana donde se deben buscar los widgets con foco.
        """
        menu_editar = tk.Menu(barra_padre, tearoff=0)

        def lanzar(evento):
            """
            Función interna que localiza el widget activo en la ventana objetivo
            y le envía el evento virtual de edición.
            """
            widget = ventana_objetivo.focus_get()
            if widget:
                try:
                    # Ejecutamos la acción (Deshacer, Copiar, etc.)
                    widget.event_generate(evento)
                except tk.TclError:
                    pass
            # 'break' evita que el evento se propague a otros bindings de la ventana
            return "break"

            # --- Comandos de Edición Estándar ---

        # El 'accelerator' es solo texto informativo para el usuario
        menu_editar.add_command(label="Deshacer", accelerator="Ctrl+Z",
                                command=lambda: lanzar("<<Undo>>"))
        menu_editar.add_command(label="Rehacer", accelerator="Ctrl+Y",
                                command=lambda: lanzar("<<Redo>>"))

        menu_editar.add_separator()

        menu_editar.add_command(label="Cortar", accelerator="Ctrl+X",
                                command=lambda: lanzar("<<Cut>>"))
        menu_editar.add_command(label="Copiar", accelerator="Ctrl+C",
                                command=lambda: lanzar("<<Copy>>"))
        menu_editar.add_command(label="Pegar", accelerator="Ctrl+V",
                                command=lambda: lanzar("<<Paste>>"))

        # Añadimos la sección "Edición" al menú que nos pasaron por parámetro
        barra_padre.add_cascade(label="Edición", menu=menu_editar)

        # Retornamos la función 'lanzar' por si la ventana quiere vincularla a teclas físicas
        return lanzar