from flask import Flask, request
import sqlite3
import hashlib

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            username TEXT,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()

def hash_pass(password):
    return hashlib.sha256(password.encode()).hexdigest()

def add_user(username, password):
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO usuarios VALUES (?, ?)", 
                   (username, hash_pass(password)))
    conn.commit()
    conn.close()

def verify_user(username, password):
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE username=? AND password=?", 
                   (username, hash_pass(password)))
    result = cursor.fetchone()
    conn.close()
    return result

@app.route('/')
def home():
    return "Servidor activo en puerto 5000"

@app.route('/login')
def login():
    username = request.args.get('username')
    password = request.args.get('password')

    if verify_user(username, password):
        return "Login correcto"
    else:
        return "Login incorrecto"

if __name__ == '__main__':
    init_db()
    add_user("max", "1234")
    add_user("compa", "abcd")
    app.run(host='0.0.0.0', port=5000)
