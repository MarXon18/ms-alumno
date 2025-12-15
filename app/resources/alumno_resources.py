from flask import Blueprint, jsonify, request, send_file
from app import db  # Necesitamos db para iniciar el repositorio
from app.mapping.alumno_mapping import AlumnoSchema, AlumnoMapper # Importamos Schema y Mapper
from app.services.alumno_service import AlumnoService
from app.repositories.alumno_repositorio import AlumnoRepository 

alumno_bp = Blueprint('alumno', __name__)

# --- Helper para Inyección de Dependencias ---
def _get_alumno_service():
    """
    Función auxiliar para "armar" el servicio.
    Crea el Repositorio con la DB real y se lo inyecta al Servicio.
    """
    repo = AlumnoRepository(session=db.session)
    return AlumnoService(repositorio=repo)

# --- RUTAS ---

@alumno_bp.route('/alumnos', methods=['GET'])
def listar_alumnos():
    service = _get_alumno_service()
    alumnos = service.buscar_todos()
    
    # Usamos el Schema directo para listas (más rápido que iterar el Mapper)
    return jsonify(AlumnoSchema(many=True).dump(alumnos)), 200

@alumno_bp.route('/alumnos/<int:id>', methods=['GET'])
def buscar_por_id(id):
    service = _get_alumno_service()
    alumno = service.buscar_por_id(id)
    
    if alumno is None:
        return jsonify({"error": "Alumno no encontrado"}), 404
        
    # Usamos el Schema para un solo objeto
    return jsonify(AlumnoSchema().dump(alumno)), 200

@alumno_bp.route('/alumnos/<int:id>/pdf', methods=['GET'])
def get_alumno_pdf(id):
    service = _get_alumno_service()
    
    try:
        pdf_buffer = service.generar_pdf(id) 
        if pdf_buffer is None:
            return jsonify({"error": "No se encontró el alumno"}), 404

        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name=f'alumno_{id}.pdf',
            mimetype='application/pdf'
        )
    except AttributeError:
        return jsonify({"error": "Generación de PDF no implementada en el servicio"}), 501
    except Exception as e:
        return jsonify({"error": f"Error interno generando PDF: {str(e)}"}), 500



