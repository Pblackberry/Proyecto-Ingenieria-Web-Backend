from abc import ABC, abstractmethod
from Models.Core.ReportModel import EmployeeReportReponse, EmployeeReportRequest, OutstandingEmployeesRequest, OutstandingEmployeesResponse

class IReportService(ABC):
    @abstractmethod
    async def generar_reporte_empleado(self, body: EmployeeReportRequest) -> EmployeeReportReponse:
        pass

    @abstractmethod
    async def obtener_sobresalientes(self, body: OutstandingEmployeesRequest) -> OutstandingEmployeesResponse:
        pass