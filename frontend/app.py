from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import requests
import os

app = Flask(__name__)
app.secret_key = 'frontend_secret_key_2024'

BACKEND_URL = os.getenv('BACKEND_URL', 'http://localhost:5000')

@app.route('/')
def index():
    if 'token' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    try:
        response = requests.post(f'{BACKEND_URL}/login', 
                               json={'username': username, 'password': password})
        
        if response.status_code == 200:
            data = response.json()
            session['token'] = data['token']
            session['username'] = data['username']
            session['role'] = data['role']
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Credenciales inválidas')
    except:
        return render_template('login.html', error='Error de conexión')

@app.route('/dashboard')
def dashboard():
    if 'token' not in session:
        return redirect(url_for('index'))
    
    try:
        headers = {'Authorization': f'Bearer {session["token"]}'}
        response = requests.get(f'{BACKEND_URL}/resources', headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            return render_template('dashboard.html', 
                                 username=data['username'],
                                 role=data['role'],
                                 resources=data['resources'])
        else:
            session.clear()
            return redirect(url_for('index'))
    except:
        return render_template('dashboard.html', error='Error de conexión')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)