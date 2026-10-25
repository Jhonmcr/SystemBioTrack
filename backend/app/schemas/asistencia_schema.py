"""
SUMMARY:
Esquemas de validación y serialización de datos con Pydantic para el Módulo 3.
Define los contratos de datos de entrada y salida para el endpoint receptor
ADMS del reloj biométrico ZKTeco K40 y las respuestas de asistencia diaria.
"""

from datetime import datetime, date, time
from typing import Optional
from pydantic import BaseModel, Field


class MarcajeCrudoCreate(BaseModel):
    """
    SUMMARY:
    Contrato de datos de entrada para recibir una trama cruda de marcaje desde el dispositivo biométrico.
    """
    Id_Empleado_Biometrico: int = Field(
        ..., 
        alias="id_empleado_biometrico", 
        description="Identificador asignado al empleado en la memoria del dispositivo ZKTeco"
    )
    Fecha_Hora_Marcaje: datetime = Field(
        ..., 
        alias="fecha_hora_marcaje", 
        description="Estampa de tiempo del marcaje registrado"
    )
    Tipo_Marcaje: Optional[str] = Field(
        "Entrada/Salida", 
        alias="tipo_marcaje", 
        description="Tipo de marcaje reportado por el dispositivo"
    )

    class Config:
        populate_by_name = True


class MarcajeCrudoResponse(BaseModel):
    """
    SUMMARY:
    Contrato de respuesta tras registrar exitosamente la trama en la tabla marcaje_crudo.
    """
    Id_Marcaje: int = Field(..., alias="id", description="Identificador único del registro persistido")
    Id_Empleado_Biometrico: int = Field(..., alias="id_empleado_biometrico")
    Fecha_Hora_Marcaje: datetime = Field(..., alias="fecha_hora_marcaje")
    Tipo_Marcaje: Optional[str] = Field(None, alias="tipo_marcaje")

    class Config:
        from_attributes = True
        populate_by_name = True


class AsistenciaDiariaResponse(BaseModel):
    """
    SUMMARY:
    Contrato de respuesta para la información consolidada de la jornada laboral de un empleado.
    """
    Id_Asistencia: int = Field(..., alias="id")
    Empleado_Id: int = Field(..., alias="empleado_id")
    Fecha_Jornada: date = Field(..., alias="fecha")
    Hora_Entrada: Optional[time] = Field(None, alias="hora_entrada")
    Hora_Salida: Optional[time] = Field(None, alias="hora_salida")
    Minutos_Tarde: int = Field(0, alias="minutos_tarde")
    Estatus_Id: int = Field(..., alias="estatus_id")
    Modificado_Manualmente: bool = Field(False, alias="modificado_manualmente")

    class Config:
        from_attributes = True
        populate_by_name = True