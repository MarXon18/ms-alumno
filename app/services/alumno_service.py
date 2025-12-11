import io
from app.models import Alumno
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

class AlumnoService:
    def __init__(self, repositorio):
        self.repo = repositorio

    # CAMBIO IMPORTANTE: Ahora recibe un OBJETO Alumno, no un dict
    def crear_alumno(self, alumno_nuevo: Alumno) -> Alumno:
        """
        Recibe un objeto Alumno ya instanciado por el Mapper.
        """
        # 1. Validamos usando el atributo del objeto (ya no ['clave'])
        if self.repo.existe_legajo(alumno_nuevo.nro_legajo):
             raise ValueError("El legajo ya existe")

        # 2. Ya no hace falta instanciar Alumno(**data), porque ya es un objeto.
        #    Pasamos directamente el objeto al repositorio.
        return self.repo.crear(alumno_nuevo)

    def buscar_por_id(self, id: int) -> Alumno:
        alumno = self.repo.buscar_por_id(id)
        if not alumno:
            return None 
        return alumno
    
    def buscar_todos(self) -> list[Alumno]:
        """
        Recupera todos los alumnos delegando al repositorio.
        """
        return self.repo.buscar_todos()

    def actualizar_alumno(self, id: int, data_actualizada: dict) -> Alumno:
        alumno = self.repo.buscar_por_id(id)
        if not alumno:
            return None

        # Actualización dinámica y SEGURA
        for clave, valor in data_actualizada.items():
            # PROTECCIÓN: Nunca permitas actualizar el ID
            if clave == 'id':
                continue
                
            if hasattr(alumno, clave):
                setattr(alumno, clave, valor)

        # El repo se encarga de guardar (commit)
        return self.repo.actualizar(alumno)

    def borrar_por_id(self, id: int):
        return self.repo.borrar_por_id(id)

    def generar_pdf(self, id: int):
        """
        Genera un PDF en memoria (sin guardar en disco) con los datos del alumno.
        """
        alumno = self.repo.buscar_por_id(id)
        if not alumno:
            return None
        
        # Crear un buffer de memoria (IO Stream)
        buffer = io.BytesIO()
        
        # Crear el objeto PDF usando el buffer como destino
        p = canvas.Canvas(buffer, pagesize=letter)
        
        # --- Dibujar contenido en el PDF ---
        p.setTitle(f"Reporte del Alumno {alumno.nro_legajo}")
        
        # Encabezado
        p.setFont("Helvetica-Bold", 16)
        # Ajustamos coordenadas X, Y (0,0 es abajo a la izquierda)
        p.drawString(100, 750, f"Ficha de Alumno: {alumno.apellido}, {alumno.nombre}")
        
        # Datos del cuerpo
        p.setFont("Helvetica", 12)
        p.drawString(100, 700, f"Legajo: {alumno.nro_legajo}")
        p.drawString(100, 680, f"Documento: {alumno.nro_documento}")
        p.drawString(100, 660, f"Email: {getattr(alumno, 'email', 'No informado')}")
        
        # Cerrar la página y guardar en el buffer
        p.showPage()
        p.save()
        
        # Mover el puntero al inicio del buffer para que Flask pueda leerlo desde el principio
        buffer.seek(0)
        return buffer

