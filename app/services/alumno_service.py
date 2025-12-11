from app.models import Alumno

class AlumnoService:
    def __init__(self, repositorio):
        """
        Inyección de Dependencia: El servicio recibe el repositorio.
        Esto permite pasarle un repositorio FALSO (Mock) en los tests.
        """
        self.repo = repositorio

    def crear_alumno(self, data: dict) -> Alumno:
        """
        Contiene lógica de negocio antes de guardar.
        """
        # 1. Lógica de Negocio (Ejemplo)
        if self.repo.existe_legajo(data['nro_legajo']):
             raise ValueError("El legajo ya existe")

        # 2. Creación del objeto
        nuevo_alumno = Alumno(**data)
        
        # 3. Delegar persistencia al repo
        return self.repo.crear(nuevo_alumno)

    def buscar_por_id(self, id: int) -> Alumno:
        alumno = self.repo.buscar_por_id(id)
        if not alumno:
            # Manejo de errores de negocio
            return None 
        return alumno

    def actualizar_alumno(self, id: int, data_actualizada: dict) -> Alumno:
        alumno = self.repo.buscar_por_id(id)
        if not alumno:
            return None

        for clave, valor in data_actualizada.items():
            # PROTECCIÓN: Nunca permitas actualizar el ID
            if clave == 'id':
                continue
                
            if hasattr(alumno, clave):
                setattr(alumno, clave, valor)

        return self.repo.actualizar(alumno)
    def generar_pdf(self, id: int):
        alumno = self.repo.buscar_por_id(id)
        if not alumno:
            return None
        
        # Aquí va tu lógica de ReportLab usando los datos de 'alumno'
        # ...
        buffer = io.BytesIO()
        # ... generar pdf en buffer ...
        buffer.seek(0)
        return buffer
