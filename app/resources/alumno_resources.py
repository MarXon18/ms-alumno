from flask import Blueprint, jsonify, request, send_file
from app.mapping.alumno_mapping import AlumnoMapper, AlumnoSchema
from app.services.alumno_service import AlumnoService
from app.validators import validate_with
from app.models import Alumno
import logging
import io

logging.basicConfig(level=logging.DEBUG)
alumno_bp = Blueprint('alumno', __name__)

#pdf
@alumno_bp.route('/alumno/<int:id>/pdf', methods=['GET'])
def get_alumno_pdf(id):
    pdf_buffer = AlumnoService.generar_pdf(id)
    if pdf_buffer is None:
        return jsonify({"error": "No se pudo generar el PDF para el alumno o el alumno no fue encontrado"}), 404

    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=f'alumno_{id}.pdf',
        mimetype='application/pdf'
    )

#json
@alumno_bp.route('/alumno/<int:id>/json', methods=['GET'])
def get_alumno_json(id):
    alumno = AlumnoService.buscar_por_id(id)
    if alumno is None:
        return jsonify({"error": "Alumno no encontrado"}), 404
    return AlumnoSchema().dump(alumno), 200

@alumno_bp.route('/alumno/<int:id>', methods=['GET'])
def buscar_por_id(id):
    alumno= AlumnoService.buscar_por_id(id)
    if alumno is None:
        return jsonify({"error": "Alumno no encontrado"}), 404
    return AlumnoSchema().dump(alumno),200

@alumno_bp.route('/alumno', methods=['GET'])
def listar_alumnos():
    alumnos = AlumnoService.buscar_todos()
    return AlumnoSchema().dump(alumnos, many=True),200

@alumno_bp.route('/alumno', methods=['POST'])
@validate_with(AlumnoMapper)
def crear(data: Alumno):
    AlumnoService.crear_alumno(data)
    return jsonify({"mensaje": "Alumno creado correctamente"}),201

@alumno_bp.route('/alumno/<int:id>', methods=['PUT'])
@validate_with(AlumnoMapper)
def actualizar(data: Alumno, id: int):
    actualizado = AlumnoService.actualizar_alumno(id, data)
  
    if actualizado is None:
        return jsonify({"error": "Alumno no encontrado"}), 404
    return jsonify({"mensaje": "Alumno actualizado correctamente"}), 200

# DELETE /alumno/<id>
@alumno_bp.route('/alumno/<int:id>', methods= ['DELETE'])
def borrar(id):
    eliminado = AlumnoService.borrar_por_id(id)
    if eliminado is None:
        return jsonify({"error": "Alumno no encontrado"}), 404
    return jsonify({"mensaje": "Alumno eliminado correctamente"}), 200

