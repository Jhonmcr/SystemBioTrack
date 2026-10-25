"""
SUMMARY:
Modelos ORM de SQLAlchemy para el Módulo 3: Motor Biométrico y Asistencia (Core).
Mapea las tablas 'marcaje_crudo', 'estatus_asistencia' y 'asistencia_diaria'
asegurando la persistencia inmutable de tramas de red del reloj ZKTeco K40
y el registro estructurado de la jornada laboral.
"""

from sqlalchemy import Column, Integer, String, DateTime, Date, Boolean, ForeignKey, Time
from sqlalchemy.orm import relationship
from app.core.database import Base


class MarcajeCrudo(Base):
    """
    SUMMARY:
    Modelo representativo de la tabla 'marcaje_crudo'.
    Almacena de forma inmutable todas las tramas de marcaje recibidas desde el biométrico.
    """
    __tablename__ = "marcaje_crudo"

    # Identificador primario del registro de marcaje crudo
    Id_Marcaje = Column("id", Integer, primary_key=True, index=True)

    # Identificador asignado en el reloj biométrico ZKTeco (desacoplado de empleado.id)
    Id_Empleado_Biometrico = Column("id_empleado_biometrico", Integer, nullable=False, index=True)

    # Estampa de tiempo exacta registrada al colocar la huella/rostro
    Fecha_Hora_Marcaje = Column("fecha_hora_marcaje", DateTime, nullable=False)

    # Tipo de evento recibido en la trama (Entrada, Salida, Indefinido)
    Tipo_Marcaje = Column("tipo_marcaje", String(50), nullable=True)


class EstatusAsistencia(Base):
    """
    SUMMARY:
    Modelo representativo del catálogo 'estatus_asistencia'.
    Define los estados diarios admisibles (A Tiempo, Retrasado, Inasistente).
    """
    __tablename__ = "estatus_asistencia"

    # Clave primaria del catálogo de estatus
    Id_Estatus = Column("id", Integer, primary_key=True, index=True)

    # Denominación textual del estatus
    Nombre_Estatus = Column("nombre_estatus", String(50), nullable=False)

    # Relación inversa hacia las asistencias asociadas
    Asistencias_Relacion = relationship("AsistenciaDiaria", back_populates="Estatus_Relacion")


class AsistenciaDiaria(Base):
    """
    SUMMARY:
    Modelo representativo de la tabla 'asistencia_diaria'.
    Contiene la resolución del cálculo diario de entrada, salida, minutos de retraso
    y estado final consolidado por empleado y fecha.
    """
    __tablename__ = "asistencia_diaria"

    # Identificador primario de la fila de asistencia
    Id_Asistencia = Column("id", Integer, primary_key=True, index=True)

    # Clave foránea referencial hacia la tabla empleado
    Empleado_Id = Column("empleado_id", Integer, nullable=False)

    # Fecha de calendario a la que corresponde la jornada
    Fecha_Jornada = Column("fecha", Date, nullable=False)

    # Hora del primer marcaje válido de ingreso
    Hora_Entrada = Column("hora_entrada", Time, nullable=True)

    # Hora del último marcaje válido de egreso
    Hora_Salida = Column("hora_salida", Time, nullable=True)

    # Diferencia en minutos transcurridos tras agotar el margen de gracia
    Minutos_Tarde = Column("minutos_tarde", Integer, default=0)

    # Clave foránea que referencia al catálogo de estatus
    Estatus_Id = Column("estatus_id", Integer, ForeignKey("estatus_asistencia.id"), nullable=False)

    # Indicador booleano que señala si el registro fue corregido por un supervisor
    Modificado_Manualmente = Column("modificado_manualmente", Boolean, default=False)

    # Enlace relacional hacia el catálogo de estatus
    Estatus_Relacion = relationship("EstatusAsistencia", back_populates="Asistencias_Relacion")