from pydantic import BaseModel
from typing import Optional, List
from datetime import date
from Models.Core.AssistanceModel import AssistanceReport
from Models.Empleados import EmpleadosModel

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

class CompleteReport(BaseModel):
    Ano: Optional[int] = 0
    Mes: Optional[int] = 0
    Nombre: Optional[str] = None
    Apellido: Optional[str] = None
    Horas_trabajadas: Optional[int] = 0
    Horas_Extra: Optional[int] = 0
    Horas_Faltas: Optional[int] = 0
    Faltas: Optional[int] = 0
    Sueldo_mensual: Optional[float] = 0
    Score: Optional[float]=0
    
    def calc_score(self):
        score = (self.Horas_trabajadas +
                self.Horas_Extra * 1.5 -
                self.Horas_Faltas * 2.0 -
                self.Faltas*10)
        self.Score = score
        return self

class EmployeeReportReponse(BaseModel):
    Response_msg: Optional[str] = None
    Reporte: Optional[EmployeeReport] = None
    Reporte_mes_previo: Optional[EmployeeReport] = None
    
class OutstandingEmployeesRequest(BaseModel):
    Ano: Optional[int] = 0
    Mes: Optional[int] = 0
    
class OutstandingEmployeesResponse(BaseModel):
    Response_msg: Optional[str] = None
    Ano: Optional[int] = 0
    Mes: Optional[int] = 0
    Empleados: list[CompleteReport]