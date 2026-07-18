
import pymysql

# Configura aquí tus datos de conexión
host = 'sql5.freesqldatabase.com'
usuario = 'sql5833356'
contrasena = '55ujASTRDu'  # Cambia si tienes contraseña
base_de_datos = 'sql5833356'

# Función para obtener la conexión
def obtener_conexion():
    return pymysql.connect(host=host, user=usuario, password=contrasena, database=base_de_datos, cursorclass=pymysql.cursors.DictCursor)
