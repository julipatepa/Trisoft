



from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, static_folder='statics')


# Ruta para la página principal
@app.route('/')
def home():
    return render_template('index.html')

# Ruta para la página de servicios
@app.route('/services')
def services():
    return render_template('services.html')

# Ruta para la página de contacto
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Procesar el formulario de contacto
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        # Aquí puedes agregar lógica para guardar datos o enviar un correo
        print(f"Nombre: {name}, Email: {email}, Mensaje: {message}")
        return redirect(url_for('home'))
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
