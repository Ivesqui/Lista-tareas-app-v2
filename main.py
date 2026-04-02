import tkinter as tk
from servicios.tarea_servicio import TareaServicio # Importamos servicios para las tareas
from servicios.ayuda_servicio import AyudaServicio # Importamos servicios para la configuración
from controladores.tarea_controlador import TareaController # Importamos el controlador

def main():
    root = tk.Tk()

    # Nombre de la ventana principal
    root.title("Gestor de Tareas 2.0")

    # Tamaño inicial de la ventana
    root.geometry("800x600")

    # 1. Instanciamos la capa de servicios (Datos)
    tarea_servicio = TareaServicio()
    config_servicio = AyudaServicio()

    # 2. Iniciamos el controlador (Cerebro)
    # Él se encargará de crear la View y conectar los servicios
    app = TareaController(root, tarea_servicio, config_servicio)

    root.mainloop()

if __name__ == "__main__":
    main()