
import pymysql

# Configura aquí tus datos de conexión
host = 'sql5.freesqldatabase.com'
usuario = 'sql5833356'
contrasena = '55ujASTRDu'
base_de_datos = 'sql5833356'

# Función para obtener la conexión
def obtener_conexion():
    return pymysql.connect(host=host, user=usuario, password=contrasena, database=base_de_datos, cursorclass=pymysql.cursors.DictCursor)


def autenticar_usuario(username, password):
    conn = obtener_conexion()
    try:
        with conn.cursor() as cursor:
            cursor.callproc('sp_autenticar_usuario', [username, password])
            return cursor.fetchone()
    finally:
        conn.close()


def registrar_token_sesion(token, username):
    conn = obtener_conexion()
    try:
        with conn.cursor() as cursor:
            cursor.callproc('sp_registrar_token_sesion', [token, username])
        conn.commit()
    finally:
        conn.close()


def listar_peliculas(limit=None):
    conn = obtener_conexion()
    try:
        with conn.cursor() as cursor:
            cursor.callproc('sp_listar_peliculas', [limit])
            return cursor.fetchall()
    finally:
        conn.close()


def obtener_pelicula_por_id(pelicula_id):
    conn = obtener_conexion()
    try:
        with conn.cursor() as cursor:
            cursor.callproc('sp_obtener_pelicula_por_id', [pelicula_id])
            return cursor.fetchone()
    finally:
        conn.close()


def contar_peliculas():
    conn = obtener_conexion()
    try:
        with conn.cursor() as cursor:
            cursor.callproc('sp_contar_peliculas')
            fila = cursor.fetchone() or {}
            if 'total' in fila:
                return fila['total']
            if fila:
                return next(iter(fila.values()))
            return 0
    finally:
        conn.close()


def agregar_pelicula(titulo, anio, descripcion, archivo_imagen):
    conn = obtener_conexion()
    try:
        with conn.cursor() as cursor:
            cursor.callproc('sp_agregar_pelicula', [titulo, anio, descripcion, archivo_imagen])
        conn.commit()
    finally:
        conn.close()
