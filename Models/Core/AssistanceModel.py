from pydantic import BaseModel
from typing import Optional
from datetime import date

class WorkingHours(BaseModel):
    Horas_lunes: Optional[int] = None
    Horas_martes: Optional[int] = None
    Horas_miercoles: Optional[int] = None
    Horas_jueves: Optional[int] = None
    Horas_viernes: Optional[int] = None
    
class AssistanceReport(BaseModel):
    Total_hours: Optional[int] = 0
    Missed_days: Optional[int] =0
    Normal_hours: Optional[int] = 0
    Extra_hours: Optional[int] = 0
    Missed_hours: Optional[int] = 0
    
    # def new():
    #     AssistanceReport{
            
    #     }