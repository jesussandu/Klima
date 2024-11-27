import sqlite3

def listar_usuarios():
    conn = sqlite3.connect("sistema_desempeno.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, nombre, cargo, usuario FROM empleados")
    usuarios = cursor.fetchall()
    
    print("Usuarios registrados:")
    for usuario in usuarios:
        print(f"ID: {usuario[0]}, Nombre: {usuario[1]}, Cargo: {usuario[2]}, Usuario: {usuario[3]}")
    
    conn.close()

# Ejecutar listado
listar_usuarios()
