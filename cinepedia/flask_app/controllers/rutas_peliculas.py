from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.entidad_pelicula import Pelicula
from flask_app.models.entidad_comentarios import Comentario

# Muestra el dashboard con todas las películas si ha iniciado sesión
@app.route('/cine')
def dashboard():
    if 'usuario_id' not in session:
        flash("Debes iniciar sesión para acceder.", "login")
        return redirect('/')
    
    peliculas = Pelicula.obtener_todas()
    return render_template('dashboard.html', peliculas=peliculas)

# Vista para el formulario de crear una nueva película
@app.route('/cine/nueva')
def nueva_pelicula():
    if 'usuario_id' not in session:
        return redirect('/')
    return render_template('nueva_pelicula.html')

@app.route('/cine/crear', methods=['POST'])
def crear_pelicula():
    if 'usuario_id' not in session:
        return redirect('/')
    
    if not Pelicula.validar_pelicula(request.form):
        return redirect('/cine/nueva')
    
    data = {
        "nombre": request.form['nombre'],
        "director": request.form['director'],
        "fecha_estreno": request.form['fecha_estreno'],
        "sinopsis": request.form['sinopsis'],
        "usuario_id": session['usuario_id']
    }
    
    Pelicula.guardar(data)
    return redirect('/cine')

# Muestra los detalle de una película y sus comentarios
@app.route('/cine/<int:id>')
def ver_pelicula(id):
    if 'usuario_id' not in session:
        return redirect('/')
    
    pelicula = Pelicula.obtener_por_id(id)
    if not pelicula:
        return redirect('/cine')
    
    comentarios = Comentario.obtener_por_pelicula(id)
    return render_template('ver_pelicula.html', pelicula=pelicula, comentarios=comentarios)

# Vista para editar una película (solo si el usuario es el dueño)
@app.route('/cine/editar/<int:id>')
def editar_pelicula(id):
    if 'usuario_id' not in session:
        return redirect('/')
    
    pelicula = Pelicula.obtener_por_id(id)
    if not pelicula or pelicula.usuario_id != session['usuario_id']:
        return redirect('/cine')
        
    return render_template('editar_pelicula.html', pelicula=pelicula)

@app.route('/cine/actualizar/<int:id>', methods=['POST'])
def actualizar_pelicula(id):
    if 'usuario_id' not in session:
        return redirect('/')
        
    pelicula = Pelicula.obtener_por_id(id)
    if not pelicula or pelicula.usuario_id != session['usuario_id']:
        return redirect('/cine')
        
    if not Pelicula.validar_pelicula(request.form, pelicula_id=id):
        return redirect(f'/cine/editar/{id}')
        
    data = {
        "id": id,
        "nombre": request.form['nombre'],
        "director": request.form['director'],
        "fecha_estreno": request.form['fecha_estreno'],
        "sinopsis": request.form['sinopsis']
    }
    
    Pelicula.actualizar(data)
    return redirect('/cine')

# Elimina una película
@app.route('/cine/borrar/<int:id>')
def borrar_pelicula(id):
    if 'usuario_id' not in session:
        return redirect('/')
        
    pelicula = Pelicula.obtener_por_id(id)
    if pelicula and pelicula.usuario_id == session['usuario_id']:
        Pelicula.eliminar(id)
        
    return redirect('/cine')

# Guarda un nuevo comentario
@app.route('/comentario/crear', methods=['POST'])
def crear_comentario():
    if 'usuario_id' not in session:
        return redirect('/')
        
    pelicula_id = request.form['pelicula_id']
    pelicula = Pelicula.obtener_por_id(pelicula_id)
    
    if pelicula and pelicula.usuario_id == session['usuario_id']:
        flash("No puedes comentar tu propia película.", "comentario")
        return redirect(f'/cine/{pelicula_id}')
        
    if Comentario.validar_comentario(request.form):
        data = {
            "contenido": request.form['contenido'],
            "usuario_id": session['usuario_id'],
            "pelicula_id": pelicula_id
        }
        Comentario.guardar(data)
        
    return redirect(f'/cine/{pelicula_id}')

# Borra un comentario
@app.route('/comentario/borrar/<int:id>/<int:pelicula_id>')
def borrar_comentario(id, pelicula_id):
    if 'usuario_id' not in session:
        return redirect('/')
        
    comentario = Comentario.obtener_por_id(id)
    if comentario and comentario.usuario_id == session['usuario_id']:
        Comentario.eliminar(id)
        
    return redirect(f'/cine/{pelicula_id}')