
import pymysql

# Configura aquí tus datos de conexión
host = 'localhost'
usuario = 'root'
contrasena = ''  # Cambia si tienes contraseña
base_de_datos = 'videoclub'

# Función para obtener la conexión
def obtener_conexion():
    return pymysql.connect(host=host, user=usuario, password=contrasena, database=base_de_datos, cursorclass=pymysql.cursors.DictCursor)
