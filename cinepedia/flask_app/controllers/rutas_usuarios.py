from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.entidad_usuario import Usuario
from flask_app.models.entidad_pelicula import Pelicula
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    # Si ya inició sesión, lo mandamos directo al dashboard/películas
    if 'usuario_id' in session:
        return redirect('/cine')
    return render_template('index.html')

@app.route('/registro', methods=['POST'])
def registro():
    if not Usuario.validar_registro(request.form):
        return redirect('/')
    
    # Encriptar contraseña
    password_hash = bcrypt.generate_password_hash(request.form['password'])
    
    data = {
        "nombre": request.form['nombre'],
        "apellido": request.form['apellido'],
        "email": request.form['email'],
        "password": password_hash
    }
    
    usuario_id = Usuario.guardar(data)
    session['usuario_id'] = usuario_id
    session['nombre_usuario'] = request.form['nombre']
    
    return redirect('/cine')

@app.route('/login', methods=['POST'])
def login():
    usuario = Usuario.obtener_por_email(request.form['email'])
    
    if not usuario:
        flash("Correo electrónico no registrado.", "login")
        return redirect('/')
    
    if not bcrypt.check_password_hash(usuario.password, request.form['password']):
        flash("Contraseña incorrecta.", "login")
        return redirect('/')
    
    session['usuario_id'] = usuario.id
    session['nombre_usuario'] = usuario.nombre
    
    return redirect('/cine')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')