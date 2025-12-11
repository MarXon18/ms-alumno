from flask import Blueprint, jsonify, request, send_file
from app import db  # Necesitamos db para iniciar el repositorio
from app.mapping.alumno_mapping import AlumnoSchema
from app.services.alumno_service import AlumnoService
from app.repositories.alumno_repositorio import AlumnoRepository # Importante importar el Repo

alumno_bp = Blueprint('alumno', __name__)

# --- Helper para Inyección de Dependencias ---
def _get_alumno_service():
    """
    Función auxiliar para "armar" el servicio.
    Crea el Repositorio con la DB real y se lo inyecta al Servicio.
    """
    repo = AlumnoRepository(session=db.session)
    return AlumnoService(repositorio=repo)

# --- Rutas ---

@alumno_bp.route('/alumnos', methods=['GET'])
def listar_alumnos():
    # 1. Obtenemos la instancia del servicio ("viva")
    service = _get_alumno_service()
    
    # 2. Usamos el método de instancia (sin static)
    alumnos = service.buscar_todos()
    
    # 3. Retornamos JSON
    return jsonify(AlumnoSchema(many=True).dump(alumnos)), 200

@alumno_bp.route('/alumnos/<int:id>', methods=['GET'])
def buscar_por_id(id):
    service = _get_alumno_service()
    alumno = service.buscar_por_id(id)
    
    if alumno is None:
        return jsonify({"error": "Alumno no encontrado"}), 404
        
    return jsonify(AlumnoSchema().dump(alumno)), 200

# Endpoint para crear (Faltaba en tu código, necesario para probar el POST)
@alumno_bp.route('/alumnos', methods=['POST'])
def crear_alumno():
    service = _get_alumno_service()
    json_data = request.get_json()
    
    # Validamos esquema de entrada (opcional pero recomendado)
    errors = AlumnoSchema().validate(json_data)
    if errors:
        return jsonify(errors), 400

    try:
        nuevo_alumno = service.crear_alumno(json_data)
        return jsonify(AlumnoSchema().dump(nuevo_alumno)), 201
    except ValueError as e:
        # Capturamos el error de validación del servicio (ej: legajo duplicado)
        return jsonify({"error": str(e)}), 400

# PDF (Ojo: Necesitas implementar generar_pdf en el servicio nuevo)
@alumno_bp.route('/alumnos/<int:id>/pdf', methods=['GET'])
def get_alumno_pdf(id):
    service = _get_alumno_service()
    
    # Asegúrate de agregar el método 'generar_pdf' a tu clase AlumnoService refactorizada
    # Si no lo tienes, esto dará error.
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

