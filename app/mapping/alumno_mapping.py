from marshmallow import Schema, fields, post_load, validate
from app.models.alumno import Alumno

class AlumnoSchema(Schema):
    """
    Define el contrato de entrada.
    data_key='...' permite leer un campo del JSON (ej: firstName) 
    y asignarlo a un campo interno diferente (ej: nombre).
    """
    id = fields.Int(dump_only=True) # El ID lo genera la BD, no lo leemos del JSON
    
    # Mapeo de campos con cambio de nombre (CamelCase -> snake_case)
    apellido = fields.Str(required=True, data_key="lastName")
    nombre = fields.Str(required=True, data_key="firstName")
    
    nro_documento = fields.Str(required=True, data_key="documentNumber")
    
    sexo = fields.Str(required=True, validate=validate.OneOf(["M", "F", "X"]), data_key="gender")
    
    nro_legajo = fields.Int(required=True, data_key="studentFileNumber")
    
    # Manejo de Foreign Keys
    tipo_documento_id = fields.Int(required=True, data_key="documentTypeId")
    
    especialidad_id = fields.Int(required=True, data_key="specialtyId")

    @post_load
    def make_alumno(self, data, **kwargs):
        """
        Este método se ejecuta automáticamente tras una validación exitosa.
        Transforma el diccionario limpio en una instancia de SQLAlchemy.
        """
        # SQLAlchemy provee un constructor por defecto que acepta kwargs.
        return Alumno(**data)

class AlumnoMapper:
    """Fachada para utilizar el esquema"""
    
    @staticmethod
    def from_json(json_data: dict) -> Alumno:
        schema = AlumnoSchema()
        # load() valida, convierte tipos y ejecuta make_alumno
        return schema.load(json_data)

    @staticmethod
    def to_json(alumno: Alumno) -> dict:
        schema = AlumnoSchema()

        return schema.dump(alumno)

