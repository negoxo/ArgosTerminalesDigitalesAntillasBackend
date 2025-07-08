# backend/app.py
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import jwt 
from dotenv import load_dotenv
import pyodbc
import logging # <-- 1. Importa el módulo de logging
from logging.handlers import RotatingFileHandler # <-- Para rotación de archivos de log

# Cargar variables de entorno
load_dotenv()

# --- Configuración ---
TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
ISSUER = f"https://login.microsoftonline.com/{TENANT_ID}/v2.0"
AUDIENCE = CLIENT_ID
DATABASE_URL = os.getenv("DATABASE_URL")

# Inicializar Flask
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:8000"}})


# --- 2. CONFIGURACIÓN DETALLADA DE LOGS ---
# Esto establece el formato, el nivel y el destino de los logs.
log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')
logFile = 'app.log' # Nombre del archivo de log

# Configura un manejador de archivos que rota los logs cuando alcanzan 1MB, manteniendo 5 copias.
my_handler = RotatingFileHandler(logFile, mode='a', maxBytes=1*1024*1024, backupCount=5, encoding=None, delay=0)
my_handler.setFormatter(log_formatter)
my_handler.setLevel(logging.INFO) # Nivel mínimo para escribir en el archivo

# Añade el manejador al logger de la aplicación Flask
app.logger.setLevel(logging.INFO)
app.logger.addHandler(my_handler)


# --- Decorador de Autenticación (con logs añadidos) ---
def token_required(f):
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            try:
                auth_header = request.headers['Authorization']
                token = auth_header.split(" ")[1]
            except IndexError:
                app.logger.warning("Token malformado recibido.")
                return jsonify({"message": "Token malformado."}), 401

        if not token:
            app.logger.warning("Intento de acceso a ruta protegida sin token.")
            return jsonify({"message": "Token no encontrado."}), 401

        try:
            unverified_header = jwt.get_unverified_header(token)
            decoded_token = jwt.decode(
                token,
                options={"verify_signature": False},
                audience=AUDIENCE,
                issuer=ISSUER
            )
            current_user = decoded_token
        except jwt.ExpiredSignatureError:
            app.logger.warning(f"Token expirado para usuario: {decoded_token.get('name', 'N/A')}")
            return jsonify({"message": "El token ha expirado."}), 401
        except Exception as e:
            app.logger.error(f"Error al decodificar el token: {str(e)}")
            return jsonify({"message": "Token inválido.", "error": str(e)}), 401

        return f(current_user, *args, **kwargs)
    decorated.__name__ = f.__name__
    return decorated

# --- Rutas de la API (con logs añadidos) ---

@app.route("/")
def index():
    app.logger.info("Ruta de bienvenida '/' fue accedida.")
    return jsonify({"message": "El servidor Flask está funcionando correctamente."})

@app.route("/api/data")
@token_required
def get_data(current_user):
    user_name = current_user.get("name", "N/A")
    app.logger.info(f"Usuario '{user_name}' accedió a /api/data.")
    return jsonify({
        "message": "Respuesta protegida desde Flask.",
        "user_name_from_token": user_name
    })

@app.route("/api/alerts")
@token_required
def get_alerts(current_user):
    user_name = current_user.get("name", "N/A")
    app.logger.info(f"Usuario '{user_name}' está solicitando las alertas desde /api/alerts.")
    alerts = []
    try:
        conn = pyodbc.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute("SELECT TOP 5 ID, NombreMetrica, ValorActual, Unidad, FechaHora, UmbralNormal, UmbralAdvertencia FROM Alertas ORDER BY FechaHora DESC")
        
        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        
        for row in rows:
            alerts.append(dict(zip(columns, row)))

        app.logger.info(f"Se obtuvieron {len(alerts)} alertas de la base de datos.")

    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        app.logger.error(f"Error de base de datos al obtener alertas: {sqlstate} - {str(ex)}")
        return jsonify({"message": "Error al conectar o consultar la base de datos.", "error": str(ex)}), 500
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn:
            conn.close()
            
    return jsonify(alerts)

# --- Ejecución del Servidor ---
if __name__ == "__main__":
    app.logger.info("Iniciando servidor Flask...")
    app.run(host="0.0.0.0", port=5000, debug=True)