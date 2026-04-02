# Gestor de Tareas Version 2.0 (Semana 16) - Programación Orientada a Objetos

Este proyecto consiste en una aplicación de escritorio avanzada para la gestión de tareas, desarrollada como parte de la asignatura de **Programación Orientada a Objetos** en la **Universidad Estatal Amazónica**. 

La aplicación evoluciona el sistema de la Semana 15, integrando una experiencia de usuario optimizada mediante la implementación de **atajos de teclado (Key Bindings)** y una arquitectura robusta por capas (MVC/Modular).

---

## 👤 Información del Estudiante
* **Nombre:** Christian Iván Estupiñán Quintero
* **Curso:** 2do "A"
* **Institución:** Universidad Estatal Amazónica (UEA)
* **Asignatura:** Programación Orientada a Objetos

---

## 🎯 Objetivo de la Tarea
Desarrollar una versión mejorada del sistema de lista de tareas, incorporando interacción mediante eventos de teclado para optimizar la usabilidad, manteniendo estrictamente la **arquitectura modular por capas** y la separación de responsabilidades.

---

## 🚀 Características Principales

### Funcionalidades Core
* **Gestión de Tareas:** Crear, editar, marcar como completadas y eliminar tareas.
* **Filtros Avanzados:** Búsqueda por rango de fechas (Desde/Hasta) y filtrado por estado (Todas, Pendientes, Hecho).
* **Feedback Visual:** Diferenciación clara entre tareas pendientes (color azul) y completadas (color gris y tachadas).
* **Validación de Datos:** Sistema de validación de fechas para evitar errores cronológicos en la planificación.
* **Configuración:** Un menú para configurar los atajos como el usuario desee.

### Instalación rápida
Para instalar todas las librerías necesarias de una sola vez, abre tu terminal en la carpeta del proyecto y ejecuta:

```text
pip install -r requirements.txt
```

### Interacción Avanzada (Atajos de Teclado)
Se han implementado eventos mediante `.bind()` para permitir un flujo de trabajo sin necesidad de usar el mouse:
* **`Enter`**: Confirmar y guardar tarea en los formularios.
* **`E`**: Editar la tarea en los formularios.
* **`C`**: Marcar la tarea seleccionada como completada/pendiente.
* **`Delete` o `Supr`**: Eliminar la tarea seleccionada del sistema.
* **`Escape`**: Cerrar ventanas emergentes o salir de la aplicación.

---

## 🏗️ Arquitectura del Sistema
El proyecto sigue una estructura modular para garantizar la escalabilidad y el mantenimiento:

```text
Pasamos de esto: 

lista_tareas_app/
│
├── main.py                 # Punto de entrada de la aplicación
├── modelos/
│   └── tarea.py            # Definición de la entidad Tarea
├── servicios/
│   └── tarea_servicio.py   # Lógica de negocio y persistencia
├── controladores/
│   └── tarea_controller.py # Mediador entre la UI y el Servicio (Lógica de control)
└── ui/
    └── app_view.py         # Interfaz principal (Tkinter)
   
A esto:


lista_tareas_app_V2/
│
├── main.py                 # Punto de entrada: Inicializa la App, el Servicio y los Controladores.
├── modelos/
│   └── tarea.py            # Clase Tarea: Define los atributos (id, título, fechas, estado).
├── selectores/
│   └── filtrar_selector.py # Lógica de filtrado: Procesa búsquedas por fechas y estados fuera de la UI.
├── servicios/
│   ├── ayuda_servicio.py   # Lógica de soporte: Gestiona información del sistema y manuales.
│   └── tarea_servicio.py   # Persistencia: Maneja el CRUD y el almacenamiento de datos.
├── controladores/
│   ├── ayuda_controlador.py # Mediador de soporte: Gestiona diálogos de ayuda y atajos.
│   └── tarea_controlador.py # Mediador principal: Conecta la lógica de tareas con la interfaz.
└── ui/
    ├── principal_view.py   # Ventana Principal: Contiene la tabla (Treeview) y el panel de filtros.
    ├── atajos_dialog.py    # Ventana Emergente: Muestra la lista de comandos de teclado disponibles.
    ├── detalle_view.py     # Vista de Lectura: Muestra la información completa de una tarea seleccionada.
    ├── tarea_form.py       # Formulario Dinámico: Ventana para crear y editar tareas (Toplevel).
    └── menu_bar.py         # Constructor de Menús: Centraliza la barra superior (    
```
---

## 🛠️ Requisitos Técnicos
- Lenguaje: Python 3.x
- Librería GUI: Tkinter
- Componentes Adicionales: tkcalendar (para la selección visual de fechas).
