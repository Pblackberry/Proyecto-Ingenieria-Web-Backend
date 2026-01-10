from abc import ABC, abstractmethod
from Models.Core.ReportModel import EmployeeReportReponse, EmployeeReportRequest

class IReportService(ABC):
    @abstractmethod
    async def generar_reporte_empleado(self, body: EmployeeReportRequest) -> EmployeeReportReponse:
        pass
