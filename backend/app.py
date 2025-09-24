from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import hashlib
import jwt
import datetime
import os

app = Flask(__name__)
CORS(app)

JWT_SECRET = os.getenv('JWT_SECRET', 'tu_clave_secreta_jwt_2024')
DB_PATH = '/app/data/auth.db'

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT username, role FROM users WHERE username = ? AND password = ?', 
                   (username, hash_password(password)))
    user = cursor.fetchone()
    conn.close()
    return user

def generate_token(username, role):
    payload = {
        'username': username,
        'role': role,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm='HS256')

def verify_token(token):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = get_user(username, password)
    if user:
        token = generate_token(user[0], user[1])
        return jsonify({
            'success': True,
            'token': token,
            'username': user[0],
            'role': user[1]
        })
    
    return jsonify({'success': False, 'message': 'Credenciales inválidas'}), 401

@app.route('/verify', methods=['POST'])
def verify():
    token = request.headers.get('Authorization')
    if token and token.startswith('Bearer '):
        token = token[7:]
        payload = verify_token(token)
        if payload:
            return jsonify({'valid': True, 'user': payload})
    
    return jsonify({'valid': False}), 401

@app.route('/resources', methods=['GET'])
def get_resources():
    token = request.headers.get('Authorization')
    if not token or not token.startswith('Bearer '):
        return jsonify({'error': 'Token requerido'}), 401
    
    token = token[7:]
    payload = verify_token(token)
    if not payload:
        return jsonify({'error': 'Token inválido'}), 401
    
    role = payload['role']
    resources = {
        'admin': ['Dashboard Admin', 'Gestión Usuarios', 'Configuración Sistema', 'Reportes'],
        'user': ['Dashboard Usuario', 'Mi Perfil', 'Documentos'],
        'guest': ['Vista Pública']
    }
    
    return jsonify({
        'username': payload['username'],
        'role': role,
        'resources': resources.get(role, [])
    })

@app.route('/refresh', methods=['POST'])
def refresh_token():
    token = request.headers.get('Authorization')
    if not token or not token.startswith('Bearer '):
        return jsonify({'error': 'Token requerido'}), 401
    
    token = token[7:]
    payload = verify_token(token)
    if not payload:
        return jsonify({'error': 'Token inválido'}), 401
    
    new_token = generate_token(payload['username'], payload['role'])
    return jsonify({'token': new_token})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)