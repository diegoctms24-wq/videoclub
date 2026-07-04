
from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
import secrets
from datetime import datetime
from db import obtener_conexion

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


@app.route('/')
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('home.html', show_navbar=True)

@app.route('/peliculas/<id>')
@login_required
def peliculas(id):
    return render_template('peliculas.html', ID=id, show_navbar=True)

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
            conn = obtener_conexion()
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM usuarios WHERE cUsuario=%s AND cContrasena=%s AND lActivo=1", (username, password))
                user = cursor.fetchone()
                if user:
                    fecha_hora = datetime.now().strftime('%Y%m%d%H%M%S')
                    token = f'tokendiego{fecha_hora}{secrets.token_hex(32)}'
                    "INSERT INTO tokendesesion (cToken, cUsuario, dFecha) VALUES (%s, %s, %s)",
                    (token, username, datetime.now())
                    conn.commit()
                    session['logged_in'] = True
                    session['username'] = username
                    session['token'] = token
                    return redirect(url_for('home'))
                else:
                    error = 'Usuario o contraseña incorrectos'
        except Exception as e:
            error = f'Error de conexión: {e}'
        finally:
            if 'conn' in locals():
                conn.close()
    return render_template('login.html', error=error, show_navbar=False)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port = 3000, debug = True)