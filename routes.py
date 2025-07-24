from flask import Blueprint, jsonify, request
from database import fetch_data, execute_query
import logging

# Crear un Blueprint para las rutas de la API
api_bp = Blueprint('api', __name__)

# Obtener el logger de la aplicación Flask
logger = logging.getLogger(__name__)

# --- Rutas para la tabla antigua_Ticket ---
@api_bp.route('/antigua_tickets', methods=['GET'])
def get_antigua_tickets():
    logger.info("Solicitud GET recibida para /api/antigua_tickets")
    try:
        query = "SELECT * FROM antigua_Ticket"
        tickets = fetch_data(query)
        return jsonify(tickets)
    except Exception as e:
        logger.error(f"Error al obtener tickets de antigua_Ticket: {e}")
        return jsonify({"message": "Error al obtener los tickets de Antigua", "error": str(e)}), 500

@api_bp.route('/antigua_tickets/<int:ticket_number>', methods=['GET'])
def get_antigua_ticket_by_number(ticket_number):
    logger.info(f"Solicitud GET recibida para /api/antigua_tickets/{ticket_number}")
    try:
        query = "SELECT * FROM antigua_Ticket WHERE Number = ?"
        ticket = fetch_data(query, (ticket_number,))
        if ticket:
            return jsonify(ticket[0])
        else:
            logger.warning(f"Ticket con Number {ticket_number} no encontrado en antigua_Ticket.")
            return jsonify({"message": "Ticket no encontrado"}), 404
    except Exception as e:
        logger.error(f"Error al obtener ticket con Number {ticket_number} de antigua_Ticket: {e}")
        return jsonify({"message": "Error al obtener el ticket de Antigua", "error": str(e)}), 500

# --- Rutas para la tabla dominica_Ticket ---
@api_bp.route('/dominica_tickets', methods=['GET'])
def get_dominica_tickets():
    logger.info("Solicitud GET recibida para /api/dominica_tickets")
    try:
        query = "SELECT * FROM dominica_Ticket"
        tickets = fetch_data(query)
        return jsonify(tickets)
    except Exception as e:
        logger.error(f"Error al obtener tickets de dominica_Ticket: {e}")
        return jsonify({"message": "Error al obtener los tickets de Dominica", "error": str(e)}), 500

@api_bp.route('/dominica_tickets/<int:ticket_number>', methods=['GET'])
def get_dominica_ticket_by_number(ticket_number):
    logger.info(f"Solicitud GET recibida para /api/dominica_tickets/{ticket_number}")
    try:
        query = "SELECT * FROM dominica_Ticket WHERE Number = ?"
        ticket = fetch_data(query, (ticket_number,))
        if ticket:
            return jsonify(ticket[0])
        else:
            logger.warning(f"Ticket con Number {ticket_number} no encontrado en dominica_Ticket.")
            return jsonify({"message": "Ticket no encontrado"}), 404
    except Exception as e:
        logger.error(f"Error al obtener ticket con Number {ticket_number} de dominica_Ticket: {e}")
        return jsonify({"message": "Error al obtener el ticket de Dominica", "error": str(e)}), 500

# --- Rutas para la tabla maartin_Ticket ---
@api_bp.route('/maartin_tickets', methods=['GET'])
def get_maartin_tickets():
    logger.info("Solicitud GET recibida para /api/maartin_tickets")
    try:
        query = "SELECT * FROM maartin_Ticket"
        tickets = fetch_data(query)
        return jsonify(tickets)
    except Exception as e:
        logger.error(f"Error al obtener tickets de maartin_Ticket: {e}")
        return jsonify({"message": "Error al obtener los tickets de Maartin", "error": str(e)}), 500

@api_bp.route('/maartin_tickets/<int:ticket_number>', methods=['GET'])
def get_maartin_ticket_by_number(ticket_number):
    logger.info(f"Solicitud GET recibida para /api/maartin_tickets/{ticket_number}")
    try:
        query = "SELECT * FROM maartin_Ticket WHERE Number = ?"
        ticket = fetch_data(query, (ticket_number,))
        if ticket:
            return jsonify(ticket[0])
        else:
            logger.warning(f"Ticket con Number {ticket_number} no encontrado en maartin_Ticket.")
            return jsonify({"message": "Ticket no encontrado"}), 404
    except Exception as e:
        logger.error(f"Error al obtener ticket con Number {ticket_number} de maartin_Ticket: {e}")
        return jsonify({"message": "Error al obtener el ticket de Maartin", "error": str(e)}), 500


# --- Rutas para la tabla Thomas_Ticket ---
@api_bp.route('/thomas_tickets', methods=['GET'])
def get_thomas_tickets():
    logger.info("Solicitud GET recibida para /api/thomas_tickets")
    try:
        query = "SELECT * FROM Thomas_Ticket"
        tickets = fetch_data(query)
        return jsonify(tickets)
    except Exception as e:
        logger.error(f"Error al obtener tickets de Thomas_Ticket: {e}")
        return jsonify({"message": "Error al obtener los tickets de Thomas", "error": str(e)}), 500

@api_bp.route('/thomas_tickets/<int:ticket_number>', methods=['GET'])
def get_thomas_ticket_by_number(ticket_number):
    logger.info(f"Solicitud GET recibida para /api/thomas_tickets/{ticket_number}")
    try:
        query = "SELECT * FROM Thomas_Ticket WHERE Number = ?"
        ticket = fetch_data(query, (ticket_number,))
        if ticket:
            return jsonify(ticket[0])
        else:
            logger.warning(f"Ticket con Number {ticket_number} no encontrado en Thomas_Ticket.")
            return jsonify({"message": "Ticket no encontrado"}), 404
    except Exception as e:
        logger.error(f"Error al obtener ticket con Number {ticket_number} de Thomas_Ticket: {e}")
        return jsonify({"message": "Error al obtener el ticket de Thomas", "error": str(e)}), 500


# --- Endpoints de ejemplo pre-existentes (mantener si son necesarios) ---

# Endpoint para obtener todos los ítems
@api_bp.route('/items', methods=['GET'])
def get_items():
    logger.info("Solicitud GET recibida para /api/items")
    try:
        query = "SELECT Id, Name, Description FROM Items" # Ajusta tu tabla y columnas
        items = fetch_data(query)
        return jsonify(items)
    except Exception as e:
        logger.error(f"Error al obtener ítems: {e}")
        return jsonify({"message": "Error al obtener los ítems", "error": str(e)}), 500

# Endpoint para obtener un ítem por ID
@api_bp.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    logger.info(f"Solicitud GET recibida para /api/items/{item_id}")
    try:
        query = "SELECT Id, Name, Description FROM Items WHERE Id = ?"
        item = fetch_data(query, (item_id,))
        if item:
            return jsonify(item[0])
        else:
            logger.warning(f"Ítem con ID {item_id} no encontrado.")
            return jsonify({"message": "Ítem no encontrado"}), 404
    except Exception as e:
        logger.error(f"Error al obtener ítem con ID {item_id}: {e}")
        return jsonify({"message": "Error al obtener el ítem", "error": str(e)}), 500

# Endpoint para añadir un nuevo ítem
@api_bp.route('/items', methods=['POST'])
def add_item():
    logger.info("Solicitud POST recibida para /api/items")
    try:
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')

        if not name:
            logger.warning("Faltan datos en la solicitud POST para añadir ítem (nombre).")
            return jsonify({"message": "Nombre del ítem es requerido"}), 400

        query = "INSERT INTO Items (Name, Description) VALUES (?, ?)"
        rows_affected = execute_query(query, (name, description))
        
        if rows_affected > 0:
            logger.info(f"Ítem '{name}' añadido exitosamente.")
            return jsonify({"message": "Ítem añadido exitosamente", "name": name}), 201
        else:
            logger.error(f"No se pudo añadir el ítem '{name}'. Filas afectadas: {rows_affected}")
            return jsonify({"message": "No se pudo añadir el ítem"}), 500

    except Exception as e:
        logger.error(f"Error al añadir ítem: {e}")
        return jsonify({"message": "Error al añadir el ítem", "error": str(e)}), 500

# Endpoint para actualizar un ítem
@api_bp.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    logger.info(f"Solicitud PUT recibida para /api/items/{item_id}")
    try:
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')

        if not name and not description:
            logger.warning("No hay datos para actualizar en la solicitud PUT para ítem.")
            return jsonify({"message": "Proporcione al menos un campo (nombre o descripción) para actualizar"}), 400

        updates = []
        params = []
        if name:
            updates.append("Name = ?")
            params.append(name)
        if description:
            updates.append("Description = ?")
            params.append(description)
        
        if not updates:
            return jsonify({"message": "No hay datos válidos para actualizar"}), 400

        query = f"UPDATE Items SET {', '.join(updates)} WHERE Id = ?"
        params.append(item_id)

        rows_affected = execute_query(query, tuple(params))

        if rows_affected > 0:
            logger.info(f"Ítem con ID {item_id} actualizado exitosamente.")
            return jsonify({"message": "Ítem actualizado exitosamente"}), 200
        else:
            logger.warning(f"Ítem con ID {item_id} no encontrado para actualizar o no se realizaron cambios.")
            return jsonify({"message": "Ítem no encontrado o no se realizaron cambios"}), 404
    except Exception as e:
        logger.error(f"Error al actualizar ítem con ID {item_id}: {e}")
        return jsonify({"message": "Error al actualizar el ítem", "error": str(e)}), 500

# Endpoint para eliminar un ítem
@api_bp.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    logger.info(f"Solicitud DELETE recibida para /api/items/{item_id}")
    try:
        query = "DELETE FROM Items WHERE Id = ?"
        rows_affected = execute_query(query, (item_id,))

        if rows_affected > 0:
            logger.info(f"Ítem con ID {item_id} eliminado exitosamente.")
            return jsonify({"message": "Ítem eliminado exitosamente"}), 200
        else:
            logger.warning(f"Ítem con ID {item_id} no encontrado para eliminar.")
            return jsonify({"message": "Ítem no encontrado"}), 404
    except Exception as e:
        logger.error(f"Error al eliminar ítem con ID {item_id}: {e}")
        return jsonify({"message": "Error al eliminar el ítem", "error": str(e)}), 500