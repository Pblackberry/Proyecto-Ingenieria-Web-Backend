
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class HorarioRequest(BaseModel):
    Fecha_inicio: Optional[date] = None
    Fecha_final: Optional[date] = None
    Cedula_empleado: Optional[str] = None
    Horas_lunes: Optional[int] = None
    Horas_martes: Optional[int] = None
    Horas_miercoles: Optional[int] = None
    Horas_jueves: Optional[int] = None
    Horas_viernes: Optional[int] = None

class Horario(BaseModel):
    Nombre_empleado: Optional[str] = None
    Apellido_empleado: Optional[str] = None
    Fecha_inicio: Optional[date] = None
    Fecha_final: Optional[date] = None
    Horas_lunes: Optional[int] = None
    Horas_martes: Optional[int] = None
    Horas_miercoles: Optional[int] = None
    Horas_jueves: Optional[int] = None
    Horas_viernes: Optional[int] = None
    
    def __init__(self):
        self.Nombre_empleado = None,
        self.Apellido_empleado = None,
        self.Fecha_inicio = None,
        self.Fecha_final = None,
        self.Horas_lunes = None,
        self.Horas_martes = None,
        self.Horas_miercoles = None,
        self.Horas_jueves = None,
        self.Horas_viernes = None
    
    def set_horas_lunes(self, horas: int):
        self.Horas_lunes = horas
        return self
    
    def set_horas_martes(self, horas: int):
        self.Horas_martes = horas
        return self
    
    def set_horas_miercoles(self, horas: int):
        self.Horas_miercoles = horas
        return self
    
    def set_horas_jueves(self, horas: int):
        self.Horas_jueves = horas
        return self
    
    def set_horas_viernes(self, horas: int):
        self.Horas_viernes = horas
        return self
    
class AsistenciaRequest(BaseModel):
    Cedula: Optional[str] = None
    Fecha_inicio: Optional[date] = None
    Horas_lunes: Optional[int] = None
    Horas_martes: Optional[int] = None
    Horas_miercoles: Optional[int] = None
    Horas_jueves: Optional[int] = None
    Horas_viernes: Optional[int] = None