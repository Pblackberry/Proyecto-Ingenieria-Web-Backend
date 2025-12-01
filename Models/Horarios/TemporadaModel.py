from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class Temporada(BaseModel):
    nombre: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_final: Optional[date] = None
    mult_staff: Optional[float] = 1
    mult_manager: Optional[float] = 1
    mult_supervisor: Optional[float] = 1
    mult_as: Optional[float] = 1
    mult_foods: Optional[float] = 1
    mult_games: Optional[float] = 1
    mult_rides: Optional[float] = 1
    mult_hk: Optional[float] = 1
    mult_maintainance: Optional[float] = 1
    mult_lifeguard: Optional[float] = 1
