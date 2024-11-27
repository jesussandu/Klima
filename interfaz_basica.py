import tkinter as tk

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Mi Primera Interfaz")  # Título de la ventana
ventana.geometry("400x300")  # Tamaño de la ventana (ancho x alto)
ventana.configure(bg="lightblue")  # Fondo de la ventana

# Agregar una etiqueta
tk.Label(ventana, text="¡Hola, Mundo!", font=("Arial", 16, "bold"), bg="lightblue", fg="darkblue").pack(pady=20)

# Agregar un botón
def boton_presionado():
    print("¡Botón presionado!")
    tk.Label(ventana, text="¡Gracias por presionar el botón!", bg="lightblue", fg="green").pack(pady=10)

tk.Button(ventana, text="Presiona Aquí", font=("Arial", 12), bg="#4CAF50", fg="white", command=boton_presionado).pack(pady=20)

# Iniciar el bucle principal
ventana.mainloop()
