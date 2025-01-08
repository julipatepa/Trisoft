from flask import Flask, render_template, request, redirect, url_for, session
from functools import wraps

app = Flask(__name__, static_folder='statics')

# Almacenamiento temporal de clientes
clients = []
client_id = 1

# Clave secreta para la sesión
app.secret_key = 'your_secret_key'

# Función para proteger rutas privadas
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
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
        # Procesar el formulario de contacto
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        # Guardar los datos (simulado en la memoria)
        global client_id
        client = {
            'id': client_id,
            'name': name,
            'email': email,
            'message': message
        }
        clients.append(client)
        client_id += 1

        # Mostrar un mensaje de éxito o permanecer en la misma página
        return render_template('contact.html', message="Mensaje enviado correctamente")

    return render_template('contact.html')

# Ruta para iniciar sesión (solo para el desarrollador)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Verificar si las credenciales son correctas (esto es solo un ejemplo)
        if username == 'admin' and password == 'admin':
            session['logged_in'] = True
            return redirect(url_for('clients_page'))
        else:
            return 'Credenciales incorrectas', 403

    return render_template('login.html')

# Ruta para mostrar la lista de clientes (solo accesible por el desarrollador)
@app.route('/clients')
@login_required
def clients_page():
    return render_template('clients.html', clients=clients)

if __name__ == '__main__':
    app.run(debug=True)
