import tkinter as tk
from tkinter import simpledialog, messagebox


class AtajosDialog:
    """
    Ventana emergente (Toplevel) para la personalización de atajos de teclado.
    Permite al usuario ver las teclas actuales y reasignarlas mediante cuadros de diálogo.
    """

    def __init__(self, app_instance):
        """
        Constructor del diálogo de atajos.
        app_instancia: Referencia a la aplicación principal (Controlador) para acceder a los servicios.
        """
        self.app = app_instance

        # Crear la ventana sobre la raíz (root)
        self.ventana = tk.Toplevel(app_instance.root)
        self.ventana.title("Configurar Atajos")
        self.ventana.geometry("400x350")

        # --- Configuración de Modalidad ---
        # transient: Hace que la ventana dependa de la principal (si se minimiza la principal, esta también)
        self.ventana.transient(app_instance.root)
        # grab_set: Bloquea eventos en la ventana principal hasta que se cierre esta (ventana modal)
        self.ventana.grab_set()

        # Dibujar los elementos visuales
        self._dibujar()

    def _dibujar(self):
        """
        Consulta los atajos actuales y genera la lista de botones de forma dinámica.
        """
        # 1. Obtenemos el diccionario de atajos desde el servicio (ej: {'borrar': 'Delete', ...})
        atajos = self.app.config_servicio.obtener_atajos()

        # Título de la ventana
        tk.Label(self.ventana, text="Personalizar Atajos de Teclado",
                 font=("Arial", 11, "bold")).pack(pady=15)

        # Contenedor central para organizar las etiquetas y botones en rejilla (grid)
        frame_grid = tk.Frame(self.ventana)
        frame_grid.pack(padx=30, pady=10, fill="both", expand=True)

        # 2. Generar filas dinámicamente según la cantidad de atajos configurados
        # Usamos enumerate para saber en qué fila (idx) colocar cada elemento
        for idx, (accion, tecla) in enumerate(atajos.items()):
            # Etiqueta descriptiva (Nombre de la acción)
            # .capitalize() pone la primera letra en mayúscula (ej: "borrar" -> "Borrar")
            tk.Label(frame_grid, text=f"{accion.capitalize()}:",
                     font=("Arial", 9, "bold")).grid(row=idx, column=0, sticky="e", pady=8, padx=5)

            # Botón que muestra la tecla actual asignada.
            # Al hacer clic, ejecuta _procesar_cambio pasando el nombre de la acción.
            # Nota: a=accion captura el valor actual en cada iteración del bucle.
            btn = tk.Button(frame_grid, text=tecla, width=15, bg="#ffffff", relief="groove",
                            command=lambda a=accion: self._procesar_cambio(a))
            btn.grid(row=idx, column=1, pady=8, padx=10, sticky="w")

        # Botón inferior para cerrar el diálogo
        tk.Button(self.ventana, text="Cerrar", command=self.ventana.destroy,
                  width=12, bg="#e0e0e0").pack(pady=20)

    def _procesar_cambio(self, accion):
        """
        Muestra un cuadro de entrada para que el usuario escriba la nueva combinación de teclas.
        accion: Nombre de la función a la que se le cambiará el atajo.
        """
        # Abrir un diálogo de entrada de texto simple
        nueva = simpledialog.askstring("Cambiar Atajo",
                                       f"Escribe la nueva tecla para '{accion}':\n"
                                       f"(Ejemplos: F2, <Control-k>, <Delete>, <Alt-a>)")

        # Si el usuario no canceló el diálogo (nueva no es None)
        if nueva is not None:
            nueva = nueva.strip()  # Limpiar espacios en blanco

            # Validación: No permitir atajos vacíos
            if not nueva:
                messagebox.showwarning("Error", "El atajo no puede estar vacío.")
            else:
                # 1. Persistencia: Guardar el cambio en el archivo de configuración a través del servicio
                self.app.config_servicio.actualizar_atajo(accion, nueva)

                # 2. Aplicación: Notificar al Manager que debe refrescar los 'binds'
                # en la ventana principal para que la nueva tecla funcione de inmediato.
                self.app.config_manager.vincular_atajos()

                # 3. Interfaz: Cerramos la ventana actual y la volvemos a abrir
                # para que el usuario vea reflejada la nueva tecla en el botón.
                self.ventana.destroy()
                AtajosDialog(self.app)