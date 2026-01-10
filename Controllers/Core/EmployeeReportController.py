from fastapi import APIRouter, Depends
from Models.Core.ReportModel import EmployeeReportRequest, EmployeeReportReponse
from Interfaces.IReportService import IReportService
from Services.ReportService import SqlReportService

router = APIRouter(prefix="/core/generate-report", tags=["Core"])

def get_report_service() -> IReportService:
    return SqlReportService()

@router.post("/obtener-reporte")
async def obtener_reporte(
    body: EmployeeReportRequest,
    service: IReportService = Depends(get_report_service)
):
    return await service.generar_reporte_empleado(body)
    
    