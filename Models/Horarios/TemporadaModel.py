from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class Temporada(BaseModel):
    nombre: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_final: Optional[date] = None
    mult_staff: Optional[float] = None
    mult_manager: Optional[float] = None
    mult_supervisor: Optional[float] = None
    mult_as: Optional[float] = None
    mult_foods: Optional[float] = None
    mult_games: Optional[float] = None
    mult_rides: Optional[float] = None
    mult_hk: Optional[float] = None
    mult_maintainance: Optional[float] = None
    mult_lifeguard: Optional[float] = None
