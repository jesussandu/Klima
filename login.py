import tkinter as tk
import os
import sys
import sqlite3
from tkinter import messagebox
from admin_panel import show_admin_panel
from employee_panel import show_employee_panel
import globals  # Importamos el archivo globals.py para el ID del empleado
from PIL import Image, ImageTk  

if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS  # PyInstaller extrae los archivos aquí
else:
    base_path = os.path.abspath(".")

# Ruta de la base de datos
db_path = os.path.join(base_path, "sistema_desempeno.db")

# Función para inicializar la base de datos con datos por defecto
def inicializar_base_datos():
    conn = sqlite3.connect(db_path)  # Conexión a la base de datos
    cursor = conn.cursor()

    # Crear la tabla de empleados si no existe
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS empleados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT NOT NULL,
        contrasena TEXT NOT NULL,
        cargo TEXT NOT NULL
    )''')

    # Verificar si ya hay datos en la tabla
    cursor.execute('SELECT COUNT(*) FROM empleados')
    cantidad = cursor.fetchone()[0]

    if cantidad == 0:  # Si no hay datos, insertar usuarios por defecto
        # Agregar usuarios de ejemplo (usuarios y contraseñas por defecto)
        empleados = [
            ('admin', 'admin123', 'gerente'),
            ('juan', 'juan123', 'empleado'),
            ('maria', 'maria123', 'empleado')
        ]

        cursor.executemany('''
        INSERT INTO empleados (usuario, contrasena, cargo)
        VALUES (?, ?, ?)''', empleados)

        conn.commit()  # Guardar los cambios

    conn.close() 

def validar_usuario(usuario, contrasena):
    conn = sqlite3.connect(db_path)  # Conexión a la base de datos usando db_path
    cursor = conn.cursor()

    cursor.execute("SELECT id, cargo FROM empleados WHERE usuario = ? AND contrasena = ?", (usuario, contrasena))
    resultado = cursor.fetchone()
    conn.close()

    if resultado:
        globals.id_empleado_logueado = resultado[0]
        return resultado[1]  # Retorna el cargo (gerente o empleado)
    else:
        return None

def login():
    usuario = entry_usuario.get()
    contrasena = entry_contrasena.get()
    cargo = validar_usuario(usuario, contrasena)

    if cargo == "gerente":
        ventana.destroy()
        show_admin_panel()
    elif cargo == "empleado":
        ventana.destroy()
        show_employee_panel()
    else:
        messagebox.showerror("Acceso denegado", "Usuario o contraseña incorrectos.")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Sistema de Gestión - Inicio de Sesión")
ventana.geometry("500x500")
ventana.configure(bg="white")  

# Título
tk.Label(ventana, text="Bienvenido al Sistema de Gestión", font=("Helvetica", 18, "bold"), bg="white", fg="#333333").pack(pady=20)

if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.abspath(".")

logo_path = os.path.join(base_path, "logo.png")

try:
    logo = Image.open(logo_path)  # Cargar el logo usando la ruta correcta
    logo_resized = logo.resize((150, 150))  # Redimensionar el logo si es necesario
    logo_tk = ImageTk.PhotoImage(logo_resized)
    tk.Label(ventana, image=logo_tk, bg="white").pack(pady=10)
except FileNotFoundError:
    tk.Label(ventana, text="Logo no encontrado", font=("Arial", 12, "italic"), bg="white", fg="red").pack(pady=10)

# Formulario de inicio de sesión
tk.Label(ventana, text="Usuario:", font=("Arial", 12), bg="white").pack(pady=5)
entry_usuario = tk.Entry(ventana, font=("Arial", 12), width=30)
entry_usuario.pack(pady=5)

tk.Label(ventana, text="Contraseña:", font=("Arial", 12), bg="white").pack(pady=5)
entry_contrasena = tk.Entry(ventana, font=("Arial", 12), show="*", width=30)
entry_contrasena.pack(pady=5)

# Botón de inicio de sesión
tk.Button(ventana, text="Iniciar Sesión", font=("Arial", 12), bg="#4CAF50", fg="white", activebackground="#45a049", padx=20, pady=5, command=login).pack(pady=20)

# Ejecutar el bucle principal
ventana.mainloop()
