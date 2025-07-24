import pyodbc
from flask import current_app # Para acceder a la configuración de la app
import logging
import base64 # Importa base64 para el manejo de datos IMAGE

# Obtener el logger de la aplicación Flask
logger = logging.getLogger(__name__)

def get_db_connection():
    """Establece y devuelve una conexión a la base de datos Azure SQL."""
    conn = None
    try:
        conn = pyodbc.connect(current_app.config['SQLALCHEMY_DATABASE_URI'])
        conn.autocommit = True # Opcional: para que cada comando se guarde inmediatamente
        logger.info("Conexión a la base de datos Azure SQL exitosa.")
        return conn
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        logger.error(f"Error al conectar a la base de datos: {sqlstate} - {ex}")
        raise # Relanza la excepción para que sea manejada por la ruta
    except Exception as e:
        logger.error(f"Error inesperado en get_db_connection: {e}")
        raise # Relanza la excepción

def fetch_data(query, params=None):
    """Ejecuta una consulta SELECT y devuelve los resultados."""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        results = []
        for row in cursor.fetchall():
            formatted_row = []
            for i, item in enumerate(row):
                # Si la columna es 'Signature' y el ítem es bytes/memoryview, convertir a Base64
                if columns[i] == 'Signature' and isinstance(item, (bytes, memoryview)):
                    formatted_row.append(base64.b64encode(item).decode('utf-8')) # Convertir a Base64
                elif isinstance(item, (bytes, memoryview)):
                    # Para otros tipos binarios que no son Signature, puedes convertirlos a hex o ignorarlos
                    formatted_row.append(item.hex()) 
                else:
                    formatted_row.append(str(item)) # Convertir todos los demás a string para JSON
            results.append(dict(zip(columns, formatted_row)))
        logger.debug(f"Datos obtenidos con la consulta: {query} con parámetros {params}")
        return results
    except Exception as e:
        logger.error(f"Error al ejecutar fetch_data con query '{query}' y params '{params}': {e}")
        raise
    finally:
        if conn:
            conn.close()
            logger.debug("Conexión a la base de datos cerrada después de fetch_data.")

def execute_query(query, params=None):
    """Ejecuta una consulta INSERT, UPDATE o DELETE."""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        rows_affected = cursor.rowcount
        conn.commit() # Asegura que los cambios se guarden
        logger.info(f"Consulta ejecutada exitosamente. Filas afectadas: {rows_affected}. Consulta: {query} con parámetros {params}")
        return rows_affected
    except Exception as e:
        logger.error(f"Error al ejecutar execute_query con query '{query}' y params '{params}': {e}")
        if conn:
            conn.rollback() # Revierte los cambios si hay un error
            logger.warning("Rollback de la transacción debido a un error.")
        raise
    finally:
        if conn:
            conn.close()
            logger.debug("Conexión a la base de datos cerrada después de execute_query.")