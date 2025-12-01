from pydantic import BaseModel
from typing import Optional
from datetime import date
from Models.Core.AssistanceModel import AssistanceReport

class EmployeeReportRequest(BaseModel):
    Cedula: Optional[str] = None
    Fecha_inicio: Optional[date] = None
    
class Salary(BaseModel):
    Normal_hours: Optional[float] = None
    Extra_hours: Optional[float] = None
    Payment: Optional[float] = None
    Payment_with_mult: Optional[float] = None
    
class EmployeeReport(BaseModel):
    Ano: Optional[int] = 0
    Mes: Optional[int] = 0
    Cedula: Optional[str] = None
    Horas_trabajadas: Optional[int] = 0
    Horas_Extra: Optional[int] = 0
    Horas_Faltas: Optional[int] = 0
    Faltas: Optional[int] = 0
    Sueldo_mensual: Optional[float] = 0

class EmployeeReportReponse(BaseModel):
    Response_msg: Optional[str] = None
    Reporte: Optional[EmployeeReport] = None
    Reporte_mes_previo: Optional[EmployeeReport] = None