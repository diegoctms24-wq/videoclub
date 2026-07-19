
from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
import secrets
from datetime import datetime
import os
from db import (
    autenticar_usuario,
    registrar_token_sesion,
    listar_peliculas,
    obtener_pelicula_por_id,
    contar_peliculas,
    agregar_pelicula as db_agregar_pelicula,
)

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Cambia esto por una clave segura en producción


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            flash('Debes iniciar sesión')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def _resolver_imagen_pelicula(archivo_imagen, titulo):
    if archivo_imagen:
        ruta_local = os.path.join(app.static_folder, 'img', 'peliculas', archivo_imagen)
        if os.path.exists(ruta_local):
            return f"img/peliculas/{archivo_imagen}", True

    texto = titulo.replace(" ", "+")
    return f"https://via.placeholder.com/300x450/202632/f5f7fa?text={texto}", False


def obtener_peliculas(limit=None):
    filas = listar_peliculas(limit)

    peliculas = []
    for fila in filas:
        imagen, es_local = _resolver_imagen_pelicula(fila['archivo_imagen'], fila['titulo'])
        peliculas.append({
            'id': fila['id'],
            'titulo': fila['titulo'],
            'anio': fila['anio'],
            'descripcion': fila['descripcion'],
            'imagen': imagen,
            'es_local': es_local
        })
    return peliculas


def obtener_total_peliculas():
    return contar_peliculas()


@app.route('/')
@login_required
def home():
    peliculas_recientes = obtener_peliculas(limit=4)
    total_peliculas = obtener_total_peliculas()
    return render_template(
        'home.html',
        show_navbar=True,
        current_page='home',
        peliculas_recientes=peliculas_recientes,
        total_peliculas=total_peliculas
    )


@app.route('/peliculas/agregar', methods=['POST'])
@login_required
def agregar_pelicula():
    titulo = (request.form.get('titulo') or '').strip()
    anio = (request.form.get('anio') or '').strip()
    descripcion = (request.form.get('descripcion') or '').strip()
    archivo_imagen = (request.form.get('archivo_imagen') or '').strip()

    if not titulo or not anio or not descripcion:
        flash('Completa titulo, anio y descripcion para agregar una pelicula')
        return redirect(url_for('home'))

    if not anio.isdigit():
        flash('El anio debe contener solo numeros')
        return redirect(url_for('home'))

    db_agregar_pelicula(titulo, int(anio), descripcion, archivo_imagen or None)

    flash('Pelicula agregada correctamente')
    return redirect(url_for('home'))


@app.route('/peliculas')
@login_required
def peliculas_lista():
    peliculas = obtener_peliculas()
    return render_template('peliculas.html', show_navbar=True, current_page='peliculas', peliculas=peliculas)

@app.route('/peliculas/<id>')
@login_required
def pelicula_detalle(id):
    fila = obtener_pelicula_por_id(id)

    if fila is None:
        flash('La pelicula solicitada no existe')
        return redirect(url_for('peliculas_lista'))

    imagen, es_local = _resolver_imagen_pelicula(fila['archivo_imagen'], fila['titulo'])
    pelicula = {
        'id': fila['id'],
        'titulo': fila['titulo'],
        'anio': fila['anio'],
        'descripcion': fila['descripcion'],
        'imagen': imagen,
        'es_local': es_local
    }

    return render_template('pelicula_detalle.html', show_navbar=True, current_page='peliculas', pelicula=pelicula)


@app.route('/acerca-de')
@login_required
def acerca_de():
    return render_template('acerca.html', show_navbar=True, current_page='acerca')


@app.route('/apoyar')
@login_required
def apoyar():
    return render_template('apoyar.html', show_navbar=True, current_page='apoyar')

@app.route('/ajax', methods=['POST', 'GET'])
@login_required
def ajax():
    id = request.form.get('ID')
    otro = request.form.get('OTRO')
    return {"val1": id, "val2": otro}

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            user = autenticar_usuario(username, password)
            if user:
                fecha_hora = datetime.now().strftime('%Y%m%d%H%M%S')
                token = f'tokendiego{fecha_hora}{secrets.token_hex(32)}'
                registrar_token_sesion(token, username)
                session['logged_in'] = True
                session['username'] = username
                session['token'] = token
                return redirect(url_for('home'))
            else:
                error = 'Usuario o contraseña incorrectos'
        except Exception as e:
            error = f'Error de conexión: {e}'
    return render_template('login.html', error=error, show_navbar=False, current_page='login')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port = 3000, debug = True)