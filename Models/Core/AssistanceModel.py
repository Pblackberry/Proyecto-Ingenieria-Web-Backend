from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class WorkingHours(BaseModel):
    Horas_lunes: Optional[int] = None
    Horas_martes: Optional[int] = None
    Horas_miercoles: Optional[int] = None
    Horas_jueves: Optional[int] = None
    Horas_viernes: Optional[int] = None
    
class AssistanceReport(BaseModel):
    Total_hours: Optional[int] = None
    Normal_hours: Optional[int] = None
    Extra_hours: Optional[int] = None
    Missed_hours: Optional[int] = None