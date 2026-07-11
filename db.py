
import pymysql

# Configura aquí tus datos de conexión
host = 'sql5.freesqldatabase.com'
usuario = 'sql5832820'
contrasena = 'JHtFcZdQ5e'  # Cambia si tienes contraseña
base_de_datos = 'sql5832820'

# Función para obtener la conexión
def obtener_conexion():
    return pymysql.connect(host=host, user=usuario, password=contrasena, database=base_de_datos, cursorclass=pymysql.cursors.DictCursor)
