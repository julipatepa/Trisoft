from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
import os

app = Flask(__name__, static_folder='statics')

# Almacenamiento temporal de clientes
clients = []
client_id = 1

# Clave secreta para la sesión (usando variable de entorno para mayor seguridad)
app.secret_key = os.getenv('SECRET_KEY', 'your_default_secret_key')

# Función para proteger rutas privadas
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session or not session['logged_in']:
            flash("Por favor, inicia sesión para acceder a esta página.")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Validar los datos enviados
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        if not name or not email or not message:
            flash("Todos los campos son obligatorios.")
            return redirect(url_for('contact'))

        # Guardar los datos en memoria
        global client_id
        client = {
            'id': client_id,
            'name': name,
            'email': email,
            'message': message
        }
        clients.append(client)
        client_id += 1

        flash("Mensaje enviado correctamente.")
        return redirect(url_for('contact'))

    return render_template('contact.html')

# Ruta para iniciar sesión (solo para el desarrollador)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Usar credenciales almacenadas de manera segura (aquí ejemplo fijo)
        admin_username = os.getenv('ADMIN_USERNAME', 'admin')
        admin_password = os.getenv('ADMIN_PASSWORD', 'admin')

        if username == admin_username and password == admin_password:
            session['logged_in'] = True
            flash("Inicio de sesión exitoso.")
            return redirect(url_for('clients_page'))
        else:
            flash("Credenciales incorrectas.", "error")
            return redirect(url_for('login'))

    return render_template('login.html')

# Ruta para cerrar sesión
@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash("Has cerrado sesión correctamente.")
    return redirect(url_for('login'))

# Ruta para mostrar la lista de clientes (solo accesible por el desarrollador)
@app.route('/clients')
@login_required
def clients_page():
    if not clients:
        flash("No hay clientes registrados aún.")
    return render_template('clients.html', clients=clients)

if __name__ == '__main__':
    app.run(debug=True)
