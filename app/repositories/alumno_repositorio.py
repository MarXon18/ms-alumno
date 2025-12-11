from app.models import Alumno

class AlumnoRepository:
    def __init__(self, session):
        """
        Ahora recibimos la sesión de base de datos al iniciar.
        Esto elimina la dependencia global de 'app.db'.
        """
        self.session = session

    def crear(self, alumno: Alumno) -> Alumno:
        self.session.add(alumno)
        self.session.commit()
        return alumno

    def buscar_por_id(self, id: int) -> Alumno:
        return self.session.query(Alumno).filter_by(id=id).first() 

    def buscar_todos(self) -> list[Alumno]:
        return self.session.query(Alumno).all()
    
    def existe_legajo(self, legajo: int) -> bool:
        """
        Método NUEVO necesario para la validación del Service.
        Verifica si ya existe un alumno con ese legajo.
        """
        # Optimizacion: Solo traemos el primer resultado, no todos.
        resultado = self.session.query(Alumno).filter_by(nro_legajo=legajo).first()
        return resultado is not None

    def actualizar(self, alumno: Alumno) -> Alumno:
        """
        Renombrado de 'actualizar_alumno' a 'actualizar' para ser más genérico.
        """
        # Hacemos merge para unir el objeto a la sesión
        alumno_actualizado = self.session.merge(alumno)
        
        # ¡CRÍTICO! Faltaba esta línea. Sin esto, no se guardan los cambios.
        self.session.commit()
        
        return alumno_actualizado
    
    def borrar_por_id(self, id: int) -> Alumno:
        alumno = self.buscar_por_id(id) # Reutilizamos nuestro propio método
        if not alumno:
            return None
        
        self.session.delete(alumno)
        self.session.commit()
        return alumno
