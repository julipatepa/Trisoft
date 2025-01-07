from flask import Blueprint, render_template, request, redirect, url_for

bp = Blueprint('main', __name__)
 
@bp.route('/')
def home():
    return render_template('index.html')

@bp.route('/services')
def services():
    return render_template('services.html')

@bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        print(f"Nombre: {name}, Email: {email}, Mensaje: {message}")
        return redirect(url_for('home'))
    return render_template('contact.html')
