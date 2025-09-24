import sqlite3
import hashlib
import os
import time

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def init_database():
    # Esperar a que el volumen esté disponible
    os.makedirs('/app/data', exist_ok=True)
    
    conn = sqlite3.connect('/app/data/auth.db')
    cursor = conn.cursor()
    
    # Crear tabla de usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')
    
    # Insertar usuarios de prueba
    users = [
        ('admin', hash_password('admin123'), 'admin'),
        ('user', hash_password('user123'), 'user'),
        ('guest', hash_password('guest123'), 'guest')
    ]
    
    cursor.executemany('INSERT OR REPLACE INTO users (username, password, role) VALUES (?, ?, ?)', users)
    
    conn.commit()
    conn.close()
    print("Base de datos inicializada correctamente")
    
    # Mantener el contenedor activo
    while True:
        time.sleep(60)

if __name__ == "__main__":
    init_database()