from abc import ABC, abstractmethod
from Models.Horarios.TemporadaModel import Temporada
from Models.Core.AssistanceModel import AssistanceReport
from Models.Core.EmployeeModel import EmployeeData
from Models.Core.ReportModel import Salary

class ISalaryStrategy(ABC):
    @abstractmethod
    def CalcMonthlyPaycheck(self, season: Temporada, assistance: AssistanceReport, employee_data: EmployeeData) -> Salary:
        pass