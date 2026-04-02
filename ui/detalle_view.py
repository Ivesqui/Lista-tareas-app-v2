import tkinter as tk
from tkinter import ttk

class DetalleView:
    def __init__(self, parent, tarea):
        self.ventana = tk.Toplevel(parent)
        # Título de la ventana con el ID para referencia rápida
        self.ventana.title(f"Detalle de Tarea #{tarea.id}")
        self.ventana.geometry("550x450")
        self.ventana.minsize(400, 350)

        # Permitir que la ventana se maximice y redimensione
        self.ventana.resizable(True, True)

        self.tarea = tarea
        self._construir_detalles()

    def _construir_detalles(self):
        # Contenedor principal con padding que se expande
        main_frame = tk.Frame(self.ventana, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Cabecera (Título de la tarea y Estado)
        header_frame = tk.Frame(main_frame)
        header_frame.pack(fill=tk.X)

        # CAMBIO: Ahora muestra el Título en lugar del ID
        tk.Label(header_frame, text=self.tarea.titulo.upper(),
                 font=("Arial", 12, "bold"), wraplength=300, justify=tk.LEFT).pack(side=tk.LEFT)

        estado_texto = "COMPLETADA" if self.tarea.completada else "PENDIENTE"
        estado_color = "green" if self.tarea.completada else "orange"
        tk.Label(header_frame, text=estado_texto, fg=estado_color,
                 font=("Arial", 10, "bold")).pack(side=tk.RIGHT)

        ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=15)

        # Cuerpo: Descripción (Usamos Text para que al maximizar se vea bien)
        tk.Label(main_frame, text="Descripción detallada:", font=("Arial", 10, "bold")).pack(anchor=tk.W)

        self.txt_desc = tk.Text(main_frame, font=("Arial", 11), wrap=tk.WORD,
                                bg="#f9f9f9", padx=10, pady=10, height=8)
        self.txt_desc.insert("1.0", self.tarea.descripcion)
        self.txt_desc.config(state=tk.DISABLED)  # Solo lectura
        self.txt_desc.pack(fill=tk.BOTH, expand=True, pady=5)

        # Pie: Fechas (Actualizado para el nuevo modelo de rango)
        footer_frame = tk.Frame(main_frame)
        footer_frame.pack(fill=tk.X, pady=10)

        # CAMBIO: Usamos fecha_inicio en lugar de fecha_creacion
        tk.Label(footer_frame, text=f"📅 Inicia: {self.tarea.fecha_inicio}",
                 font=("Arial", 9, "italic")).pack(side=tk.LEFT)

        # CAMBIO: Usamos fecha_fin en lugar de fecha_limite
        tk.Label(footer_frame, text=f"⌛ Finaliza: {self.tarea.fecha_fin}",
                 font=("Arial", 9, "bold"), fg="#d9534f").pack(side=tk.RIGHT)

        # Separador antes del botón
        ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=10)

        # Botón cerrar
        tk.Button(main_frame, text="Cerrar Detalles", command=self.ventana.destroy,
                  width=20, bg="#eeeeee", relief=tk.GROOVE).pack(pady=5)