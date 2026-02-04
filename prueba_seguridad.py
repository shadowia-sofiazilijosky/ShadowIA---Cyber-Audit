import sqlite3

def buscar_usuario():
    nombre = input("Introduce nombre: ")
    # ERROR: Inyección SQL
    query = "SELECT * FROM usuarios WHERE nombre = '" + nombre + "'"
    print("Ejecutando:", query)

def login_admin():
    # ERROR: Contraseña expuesta en el código
    password_secreta = "admin12345"
    user_input = input("Password: ")
    if user_input == password_secreta:
        print("Acceso concedido")