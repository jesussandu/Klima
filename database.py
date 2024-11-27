import sqlite3

def create_database():
    conn = sqlite3.connect("sistema_desempeno.db")
    cursor = conn.cursor()
    
    # Crear tabla de empleados
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS empleados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        cargo TEXT NOT NULL,
        usuario TEXT UNIQUE NOT NULL,
        contrasena TEXT NOT NULL
    )
    """)
    
    # Crear tabla de tareas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tareas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        descripcion TEXT NOT NULL,
        estado TEXT NOT NULL,
        id_empleado INTEGER,
        fecha_limite DATE,
        prioridad TEXT,
        FOREIGN KEY (id_empleado) REFERENCES empleados(id)
    )
    """)
    
    # Crear tabla de KPIs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS kpis (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        valor REAL NOT NULL,
        id_empleado INTEGER,
        FOREIGN KEY (id_empleado) REFERENCES empleados(id)
    )
    """)
    
    # Datos iniciales para empleados
    cursor.execute("INSERT OR IGNORE INTO empleados (nombre, cargo, usuario, contrasena) VALUES ('Admin', 'gerente', 'admin', 'admin123')")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()

def inicializar_base_de_datos():
    if not os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Crear tablas si no existen
        cursor.execute("""
        CREATE TABLE empleados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            usuario TEXT NOT NULL,
            contrasena TEXT NOT NULL,
            cargo TEXT NOT NULL
        )""")
        
        cursor.execute("""
        CREATE TABLE kpis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_empleado INTEGER NOT NULL,
            nombre TEXT NOT NULL,
            valor INTEGER NOT NULL,
            FOREIGN KEY (id_empleado) REFERENCES empleados(id)
        )""")
        
        # Insertar un usuario de ejemplo
        cursor.execute("INSERT INTO empleados (nombre, usuario, contrasena, cargo) VALUES (?, ?, ?, ?)", ("Juan Perez", "juan", "1234", "empleado"))
        cursor.execute("INSERT INTO empleados (nombre, usuario, contrasena, cargo) VALUES (?, ?, ?, ?)", ("Carlos García", "carlos", "5678", "gerente"))
        
        conn.commit()
        conn.close()

