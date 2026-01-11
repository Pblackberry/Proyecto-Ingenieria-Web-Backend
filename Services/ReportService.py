from fastapi import FastAPI, APIRouter, HTTPException
from Interfaces.IReportService import IReportService
from Managers.db_manager import DbManager
from Models.Empleados.EmpleadosModel import Empleado
from Models.Horarios import TemporadaModel, HorarioModel
from Models.Mensajes.ReturnMessage import ReturnMessage
from Controllers.Administrator.EmpleadoAdministrator import obtener_empleado
from datetime import date, timedelta
from Managers.Core import AsistenciaManager
from Models.Core.ReportModel import EmployeeReportRequest, EmployeeReport, EmployeeReportReponse
from Models.Core.EmployeeModel import EmployeeData
from Managers.Core.Strategies.SalaryStrategyFactory import SalaryStrategyFactory
import calendar

class SqlReportService(IReportService):
    async def generar_reporte_empleado(self, body: EmployeeReportRequest) -> EmployeeReportReponse:
        conn = await DbManager.get_db_connection()
        try:
            async with conn.cursor() as cursor:
                query = "EXEC sp_ObtenerEmpleadoKeyId ?"
                await cursor.execute(query, body.Cedula)
                row = await cursor.fetchone()
                if row:
                    empleado_key_id = row[0]
                else:
                    return EmployeeReportReponse(Response_msg="No hay un empleado registrado con la cedula proporcionada")
                query = "EXEC sp_ObtenerReportePersonal ?, ?, ?"
                params = (body.Cedula, body.Fecha_inicio.month, body.Fecha_inicio.year)
                await cursor.execute(query, params)
                row = await cursor.fetchone()
                if row:
                    PersonalReport = EmployeeReport(Ano=row[0], Mes=row[1], Cedula=row[2], Horas_trabajadas=row[3], Horas_Extra=row[4], Horas_Faltas=row[5], Faltas=row[6], Sueldo_mensual=row[7])
                    previews_month = body.Fecha_inicio.month - 1
                    if previews_month == 0:
                        previews_month = 12
                    previews_month_report = None
                    query = "EXEC sp_ObtenerReportePersonal ?, ?, ?"
                    params = (body.Cedula, previews_month, body.Fecha_inicio.year)
                    await cursor.execute(query, params)
                    row = await cursor.fetchone()
                    if row:
                        previews_month_report = EmployeeReport(Ano=row[0], Mes=row[1], Cedula=row[2], Horas_trabajadas=row[3], Horas_Extra=row[4], Horas_Faltas=row[5], Faltas=row[6], Sueldo_mensual=row[7])
                    response = EmployeeReportReponse(Response_msg= "Generacion de reporte exitosa", Reporte= PersonalReport, Reporte_mes_previo=previews_month_report)
                    return response
                
                query = "EXEC sp_ObtenerEmployeeData ?"
                await cursor.execute(query, body.Cedula)
                row = await cursor.fetchone()
                if row:
                    employee_data = EmployeeData(Cedula=body.Cedula, Nombre=row[0], Apellido=row[1], Cargo=row[2], Sueldo_hora=row[3], Area=row[4])
                else:
                    return EmployeeReport()
                print("Employee data: ", employee_data)
                last_month_day = calendar.monthrange(body.Fecha_inicio.year, body.Fecha_inicio.month)[1]
                las_month_date = date(body.Fecha_inicio.year, body.Fecha_inicio.month, last_month_day)
                assistance_report = await AsistenciaManager.CalculateAssistance(body.Fecha_inicio, las_month_date, body.Cedula)
                if assistance_report.Total_hours == 0:
                    return EmployeeReportReponse(Response_msg="No fue posible generar un reporte de asistencia para el reporte general")
                query = "EXEC sp_ObtenerTemporadaActual ?"
                await cursor.execute(query, body.Fecha_inicio)
                row = await cursor.fetchone()
                if row:
                    temporada_actual = TemporadaModel.Temporada(nombre=row[0], fecha_inicio=None, fecha_final=None, mult_staff=row[1], mult_supervisor=row[2], mult_manager=row[3], mult_as=row[4], mult_foods=row[5], mult_games=row[6], mult_hk=row[7], mult_maintainance=row[8], mult_rides=row[9], mult_lifeguard=row[10])
                else:
                    temporada_actual = TemporadaModel.Temporada()
                strategy = SalaryStrategyFactory.get_strategy(employee_data)
                paycheck_report = strategy.calculate_salary(temporada_actual, assistance_report, employee_data)
                final_report = EmployeeReport(Ano=int(body.Fecha_inicio.year), Mes=int(body.Fecha_inicio.month), Cedula=body.Cedula, Horas_trabajadas=assistance_report.Total_hours, Horas_Extra=assistance_report.Extra_hours, Horas_Faltas=assistance_report.Missed_hours, Faltas=assistance_report.Missed_days, Sueldo_mensual=round(paycheck_report.Payment_with_mult, 2))
                previews_month = body.Fecha_inicio.month - 1
                if previews_month == 0:
                    previews_month = 12
                previews_month_report = None
                query = "EXEC sp_ObtenerReportePersonal ?, ?, ?"
                params = (body.Cedula, previews_month, body.Fecha_inicio.year)
                await cursor.execute(query, params)
                row = await cursor.fetchone()
                if row:
                    previews_month_report = EmployeeReport(Ano=row[0], Mes=row[1], Cedula=row[2], Horas_trabajadas=row[3], Horas_Extra=row[4], Horas_Faltas=row[5], Faltas=row[6], Sueldo_mensual=row[7])
                response = EmployeeReportReponse(Response_msg="Generacion de reporte exitosa", Reporte= final_report, Reporte_mes_previo=previews_month_report)
                query = "EXEC sp_GenerarReporte ?, ?, ?, ?, ?, ?, ?, ?"
                params = (empleado_key_id, final_report.Ano, final_report.Mes, final_report.Horas_trabajadas, final_report.Horas_Extra, final_report.Horas_Faltas, final_report.Faltas, final_report.Sueldo_mensual)
                await cursor.execute(query, params)
                row = await cursor.fetchone()
                if row:
                    if row[0] == 1:
                        return EmployeeReportReponse(Response_msg="Ya existe un registro para este mesa para este empleado registrado en la bdd")
                else:
                    return EmployeeReportReponse(Response_msg="Error al intentar registrar reporte en bdd")
                return response
        except Exception as e:
            print("exception: ", str(e))
            return EmployeeReportReponse(Response_msg="Error al generar reporte")               
        finally:
            await conn.close()