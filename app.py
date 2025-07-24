# backend/app.py
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import jwt
from dotenv import load_dotenv
import logging
from logging.handlers import RotatingFileHandler

# Cargar variables de entorno
load_dotenv()

# --- Configuración ---
TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
ISSUER = f"https://login.microsoftonline.com/{TENANT_ID}/v2.0"
AUDIENCE = CLIENT_ID

# Inicializar Flask
app = Flask(__name__)

# Cargar configuración desde config.py
from config import Config
app.config.from_object(Config)

# Configura CORS para permitir solicitudes desde tu frontend Angular
# Reemplaza 'http://localhost:8000' con la URL real de tu frontend Angular en producción
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:8000", "http://127.0.0.1:8000"]}})

# --- CONFIGURACIÓN DETALLADA DE LOGS ---
log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')
log_file_path = os.path.join(os.getcwd(), 'logs', app.config['LOG_FILE']) # Ruta completa al archivo de log

# Asegúrate de que la carpeta 'logs' exista
if not os.path.exists(os.path.dirname(log_file_path)):
    os.makedirs(os.path.dirname(log_file_path))

# Configura un manejador de archivos que rota los logs cuando alcanzan 1MB, manteniendo 5 copias.
my_handler = RotatingFileHandler(log_file_path, mode='a', maxBytes=1*1024*1024, backupCount=5, encoding='utf-8', delay=0)
my_handler.setFormatter(log_formatter)
my_handler.setLevel(app.config['LOG_LEVEL']) # Nivel mínimo para escribir en el archivo

# Añade el manejador al logger de la aplicación Flask
app.logger.setLevel(app.config['LOG_LEVEL'])
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
            # Para validación completa del token, necesitarías las claves públicas de Azure AD.
            # Aquí, solo se verifica la audiencia y el emisor sin verificar la firma (para simplificar, pero NO RECOMENDADO EN PRODUCCIÓN).
            decoded_token = jwt.decode(
                token,
                options={"verify_signature": False}, # PELIGROSO en producción. Solo para depuración.
                audience=AUDIENCE,
                issuer=ISSUER
            )
            current_user = decoded_token
        except jwt.ExpiredSignatureError:
            app.logger.warning(f"Token expirado para usuario: {decoded_token.get('name', 'N/A') if 'decoded_token' in locals() else 'N/A'}")
            return jsonify({"message": "El token ha expirado."}), 401
        except Exception as e:
            app.logger.error(f"Error al decodificar el token: {str(e)}")
            return jsonify({"message": "Token inválido.", "error": str(e)}), 401

        return f(current_user, *args, **kwargs)
    decorated.__name__ = f.__name__
    return decorated

# Importa las rutas después de inicializar la aplicación para evitar problemas de importación circular
from routes import api_bp
app.register_blueprint(api_bp, url_prefix='/api') # Registra el blueprint con prefijo /api

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
    from database import fetch_data # Importar aquí para evitar importación circular con app
    user_name = current_user.get("name", "N/A")
    app.logger.info(f"Usuario '{user_name}' está solicitando las alertas desde /api/alerts.")
    try:
        # Usa la función fetch_data de database.py
        query = "SELECT TOP 5 ID, NombreMetrica, ValorActual, Unidad, FechaHora, UmbralNormal, UmbralAdvertencia FROM Alertas ORDER BY FechaHora DESC"
        alerts = fetch_data(query)
        app.logger.info(f"Se obtuvieron {len(alerts)} alertas de la base de datos.")
        return jsonify(alerts)
    except Exception as e:
        app.logger.error(f"Error al obtener alertas: {str(e)}")
        return jsonify({"message": "Error al obtener las alertas", "error": str(e)}), 500


# --- Ejecución del Servidor ---
if __name__ == "__main__":
    app.logger.info("Iniciando servidor Flask...")
    app.run(host="0.0.0.0", port=5000, debug=app.config['DEBUG']) # Usa app.config['DEBUG']