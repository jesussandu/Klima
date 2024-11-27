import os
import sys
import tkinter as tk
from tkinter import messagebox
from openpyxl import Workbook  # Para exportar a Excel
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import sqlite3

def calcular_kpi(id_empleado):
    # Calcular el KPI basado en las tareas completadas
    conn = sqlite3.connect("sistema_desempeno.db")
    cursor = conn.cursor()
    
    # Contar las tareas completadas para el empleado
    cursor.execute("""
        SELECT COUNT(*) FROM tareas
        WHERE id_empleado = ? AND estado = 'completada'
    """, (id_empleado,))
    tareas_completadas = cursor.fetchone()[0]
    
    # Calcular el KPI basado en el número de tareas completadas (puedes modificar esto según tus criterios)
    kpi_valor = tareas_completadas * 10  # Suponiendo que cada tarea completada da 10 puntos
    
    # Actualizar o insertar el KPI en la base de datos
    cursor.execute("""
        INSERT OR REPLACE INTO kpis (id_empleado, nombre, valor)
        VALUES (?, 'Desempeño', ?)
    """, (id_empleado, kpi_valor))
    
    conn.commit()
    conn.close()

def asignar_tarea():
    def guardar_tarea():
        descripcion = entry_descripcion.get()
        prioridad = entry_prioridad.get()
        fecha_limite = entry_fecha.get()
        empleado_id = entry_empleado_id.get()

        # Validar si el empleado existe
        conn = sqlite3.connect("sistema_desempeno.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM empleados WHERE id = ?", (empleado_id,))
        empleado = cursor.fetchone()
        
        if empleado:
            cursor.execute("""
                INSERT INTO tareas (descripcion, estado, id_empleado, fecha_limite, prioridad)
                VALUES (?, 'pendiente', ?, ?, ?)
            """, (descripcion, empleado_id, fecha_limite, prioridad))
            conn.commit()
            messagebox.showinfo("Éxito", "Tarea asignada correctamente")
            # Calcular y guardar el KPI después de asignar la tarea
            calcular_kpi(empleado_id)
        else:
            messagebox.showerror("Error", "El empleado no existe.")
        
        conn.close()
        ventana_tarea.destroy()

    # Crear ventana para ingresar tarea
    ventana_tarea = tk.Toplevel()
    ventana_tarea.title("Asignar Tarea")
    ventana_tarea.geometry("400x300")

    tk.Label(ventana_tarea, text="ID del Empleado:").pack(pady=5)
    entry_empleado_id = tk.Entry(ventana_tarea)
    entry_empleado_id.pack(pady=5)

    tk.Label(ventana_tarea, text="Descripción:").pack(pady=5)
    entry_descripcion = tk.Entry(ventana_tarea)
    entry_descripcion.pack(pady=5)

    tk.Label(ventana_tarea, text="Prioridad:").pack(pady=5)
    entry_prioridad = tk.Entry(ventana_tarea)
    entry_prioridad.pack(pady=5)

    tk.Label(ventana_tarea, text="Fecha Límite (YYYY-MM-DD):").pack(pady=5)
    entry_fecha = tk.Entry(ventana_tarea)
    entry_fecha.pack(pady=5)

    tk.Button(ventana_tarea, text="Guardar", command=guardar_tarea).pack(pady=20)

def ver_kpis():
    # Mostrar KPIs de los empleados
    conn = sqlite3.connect("sistema_desempeno.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT empleados.nombre, kpis.nombre, kpis.valor
        FROM kpis
        JOIN empleados ON kpis.id_empleado = empleados.id
    """)
    kpis = cursor.fetchall()
    conn.close()

    # Crear una nueva ventana para mostrar los KPIs
    ventana_kpis = tk.Toplevel()
    ventana_kpis.title("KPIs de los Empleados")
    ventana_kpis.geometry("500x400")
    ventana_kpis.configure(bg="white")

    tk.Label(ventana_kpis, text="KPIs de los Empleados", font=("Helvetica", 18, "bold"), bg="white", fg="#333333").pack(pady=20)

    if kpis:
        for fila in kpis:
            tk.Label(ventana_kpis, text=f"{fila[0]} - {fila[1]}: {fila[2]} puntos", bg="white", font=("Arial", 12)).pack(pady=5)
    else:
        tk.Label(ventana_kpis, text="No hay KPIs disponibles.", bg="white", font=("Arial", 12)).pack(pady=5)

def generar_reporte():
    # Función para generar el reporte de KPIs de todos los empleados
    conn = sqlite3.connect("sistema_desempeno.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT empleados.nombre, SUM(kpis.valor) AS total_kpi
        FROM kpis
        JOIN empleados ON kpis.id_empleado = empleados.id
        GROUP BY empleados.id
        ORDER BY total_kpi DESC
    """)
    reporte = cursor.fetchall()
    conn.close()

    # Crear una nueva ventana para mostrar el reporte
    ventana_reporte = tk.Toplevel()
    ventana_reporte.title("Reporte de Desempeño")
    ventana_reporte.geometry("500x400")
    ventana_reporte.configure(bg="white")

    tk.Label(ventana_reporte, text="Reporte de Desempeño de los Empleados", font=("Helvetica", 18, "bold"), bg="white", fg="#333333").pack(pady=20)

    if reporte:
        for fila in reporte:
            tk.Label(ventana_reporte, text=f"{fila[0]}: {fila[1]} puntos", bg="white", font=("Arial", 12)).pack(pady=5)
    else:
        tk.Label(ventana_reporte, text="No hay datos para generar el reporte.", bg="white", font=("Arial", 12)).pack(pady=5)

def exportar_reporte_excel():
    # Función para exportar el reporte a Excel
    conn = sqlite3.connect("sistema_desempeno.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT empleados.nombre, SUM(kpis.valor) AS total_kpi
        FROM kpis
        JOIN empleados ON kpis.id_empleado = empleados.id
        GROUP BY empleados.id
        ORDER BY total_kpi DESC
    """)
    reporte = cursor.fetchall()
    conn.close()

    # Crear archivo Excel
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Reporte de Desempeño"

    # Agregar encabezados
    sheet.append(["Nombre del Empleado", "Puntaje Total de KPI"])

    # Agregar datos
    for fila in reporte:
        sheet.append(fila)

    # Guardar archivo Excel
    archivo = "Reporte_Desempeño.xlsx"
    workbook.save(archivo)
    messagebox.showinfo("Éxito", f"Reporte exportado a {archivo}")

def exportar_reporte_pdf():
    # Función para exportar el reporte a PDF
    conn = sqlite3.connect("sistema_desempeno.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT empleados.nombre, SUM(kpis.valor) AS total_kpi
        FROM kpis
        JOIN empleados ON kpis.id_empleado = empleados.id
        GROUP BY empleados.id
        ORDER BY total_kpi DESC
    """)
    reporte = cursor.fetchall()
    conn.close()

    # Crear archivo PDF
    archivo = "Reporte_Desempeño.pdf"
    c = canvas.Canvas(archivo, pagesize=letter)
    c.setFont("Helvetica", 12)
    c.drawString(50, 750, "Reporte de Desempeño de los Empleados")
    c.drawString(50, 730, "---------------------------------------")

    y = 700
    for fila in reporte:
        c.drawString(50, y, f"{fila[0]}: {fila[1]} puntos")
        y -= 20
        if y < 50:
            c.showPage()
            c.setFont("Helvetica", 12)
            y = 750

    c.save()
    messagebox.showinfo("Éxito", f"Reporte exportado a {archivo}")

def show_admin_panel():
    ventana = tk.Tk()
    ventana.title("Panel de Administración")
    ventana.geometry("600x400")
    ventana.configure(bg="white")  # Fondo blanco

    # Título
    tk.Label(ventana, text="Panel de Administración", font=("Helvetica", 18, "bold"), bg="white", fg="#333333").pack(pady=20)

    # Botones con diseño atractivo
    tk.Button(ventana, text="Asignar Tareas", font=("Arial", 12), bg="#4CAF50", fg="white", activebackground="#45a049", padx=20, pady=10, command=asignar_tarea).pack(pady=10)
    tk.Button(ventana, text="Ver KPIs", font=("Arial", 12), bg="#2196F3", fg="white", activebackground="#1976D2", padx=20, pady=10, command=ver_kpis).pack(pady=10)
    tk.Button(ventana, text="Generar Reporte", font=("Arial", 12), bg="#FFC107", fg="black", activebackground="#FFA000", padx=20, pady=10, command=generar_reporte).pack(pady=10)
    tk.Button(ventana, text="Exportar a Excel", font=("Arial", 12), bg="#4CAF50", fg="white", activebackground="#45a049", padx=20, pady=10, command=exportar_reporte_excel).pack(pady=10)
    tk.Button(ventana, text="Exportar a PDF", font=("Arial", 12), bg="#FF5722", fg="white", activebackground="#E64A19", padx=20, pady=10, command=exportar_reporte_pdf).pack(pady=10)
    
    # Botón de salir
    tk.Button(ventana, text="Salir", font=("Arial", 12), bg="#F44336", fg="white", activebackground="#D32F2F", padx=20, pady=10, command=ventana.destroy).pack(pady=20)

    ventana.mainloop()
