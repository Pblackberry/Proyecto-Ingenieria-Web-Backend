from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class Temporada(BaseModel):
    nombre: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_final: Optional[date] = None
    multiplicador: Optional[float] = None
