import os
from dotenv import load_dotenv

# Carga las variables de entorno del archivo .env
load_dotenv()

class Config:
    """Clase de configuración base."""
    # Configuración de la base de datos de Azure SQL
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=your_server.database.windows.net;DATABASE=your_database;UID=your_username;PWD=your_password')
    
    # Clave secreta para la seguridad de la sesión de Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'una_cadena_secreta_muy_larga_y_aleatoria')

    # Configuración de Logging
    LOG_FILE = 'app.log'
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper() # Nivel de log: DEBUG, INFO, WARNING, ERROR, CRITICAL
    
    # DEBUG para la aplicación Flask (controla el modo de depuración de Flask)
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() in ('true', '1', 't')


class DevelopmentConfig(Config):
    """Configuración para entorno de desarrollo."""
    DEBUG = True

class ProductionConfig(Config):
    """Configuración para entorno de producción."""
    DEBUG = False
    # Podrías querer loggear a un servicio de log externo en producción