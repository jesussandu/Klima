import sqlite3
import tkinter as tk
from tkinter import messagebox
import globals

def registrar_tarea():
    conn = sqlite3.connect("sistema_desempeno.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, descripcion, estado
        FROM tareas
        WHERE estado = 'pendiente'
    """)
    tareas = cursor.fetchall()
    conn.close()

    ventana_tareas = tk.Toplevel()
    ventana_tareas.title("Registrar Tareas")
    ventana_tareas.geometry("400x300")

    tk.Label(ventana_tareas, text="Tareas Pendientes").pack(pady=10)

    for tarea in tareas:
        def completar_tarea(id_tarea):
            conn = sqlite3.connect("sistema_desempeno.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE tareas SET estado = 'completada' WHERE id = ?", (id_tarea,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Tarea completada")
            ventana_tareas.destroy()

        tk.Label(ventana_tareas, text=f"{tarea[1]} (Estado: {tarea[2]})").pack(pady=5)
        tk.Button(ventana_tareas, text="Completar", command=lambda t=tarea[0]: completar_tarea(t)).pack(pady=5)

def ver_kpis():
    # Usamos el id_empleado_logueado desde globals.py
    id_empleado = globals.id_empleado_logueado
    
    if id_empleado is None:
        messagebox.showerror("Error", "No se ha iniciado sesión correctamente.")
        return
    
    conn = sqlite3.connect("sistema_desempeno.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT nombre, valor
        FROM kpis
        WHERE id_empleado = ?
    """, (id_empleado,))
    kpis = cursor.fetchall()
    conn.close()

    ventana_kpis = tk.Toplevel()
    ventana_kpis.title("Mis KPIs")
    ventana_kpis.geometry("400x300")

    tk.Label(ventana_kpis, text="Mis KPIs").pack(pady=10)
    if kpis:
        for kpi in kpis:
            tk.Label(ventana_kpis, text=f"{kpi[0]}: {kpi[1]}").pack(pady=5)
    else:
        tk.Label(ventana_kpis, text="No se han calculado KPIs aún.").pack(pady=5)

def show_employee_panel():
    ventana = tk.Tk()
    ventana.title("Panel de Empleados")
    ventana.geometry("400x300")

    tk.Label(ventana, text="Bienvenido al Panel de Empleados").pack(pady=10)
    tk.Button(ventana, text="Registrar Tarea", command=registrar_tarea).pack(pady=10)
    tk.Button(ventana, text="Ver KPIs", command=ver_kpis).pack(pady=10)
    tk.Button(ventana, text="Salir", command=ventana.destroy).pack(pady=10)

    ventana.mainloop()