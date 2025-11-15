
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class HorarioRequest(BaseModel):
    Fecha_inicio: Optional[date] = None
    Fecha_final: Optional[date] = None
    Cedula_emplado: Optional[str] = None
    Horas_lunes: Optional[int] = None
    Horas_martes: Optional[int] = None
    Horas_miercoles: Optional[int] = None
    Horas_jueves: Optional[int] = None
    Horas_viernes: Optional[int] = None

class Horario(BaseModel):
    Fecha_inicio: Optional[date] = None
    Fecha_final: Optional[date] = None
    Empleado_id: Optional[int] = None
    Horas_lunes: Optional[int] = None
    Horas_martes: Optional[int] = None
    Horas_miercoles: Optional[int] = None
    Horas_jueves: Optional[int] = None
    Horas_viernes: Optional[int] = None