from pydantic import BaseModel
from typing import Optional
from datetime import date

class EmployeeData(BaseModel):
    Cedula: Optional[str] = None
    Nombre: Optional[str] = None
    Apellido: Optional[str] = None
    Cargo: Optional[str] = None
    Sueldo_hora: Optional[float] = None
    Area: Optional[str] = None