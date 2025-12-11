from dataclasses import dataclass
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey
from app import db
from app.models.facultad import Facultad
from app.models.documento import Documento

@dataclass(init=False, repr=True, eq=True)
class Alumno(db.Model):
    __tablename__ = 'alumnos'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    apellido: Mapped[str] = mapped_column(String(100), nullable=False)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    nro_documento: Mapped[str] = mapped_column(String(50), nullable=False)
    sexo: Mapped[str] = mapped_column(String(10), nullable=False)
    nro_legajo: Mapped[int] = mapped_column(Integer, nullable=False)
    tipo_documento_id: Mapped[int] = mapped_column(ForeignKey("documentos.id"), nullable=False)
    tipo_documento: Mapped["Documento"] = relationship("Documento", backref="alumnos")
    especialidad_id = fields.Int(required=True, data_key="specialtyId")
