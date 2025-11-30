from datetime import date
from Managers.db_manager import DbManager
from Models.Core.AssistanceModel import WorkingHours, AssistanceReport
from array import array
import calendar

async def CalculateAssistance(month: date, last_month_date: date, cedula: str) -> AssistanceReport:
    try:
        assistance_report = AssistanceReport()
        # last_month_day = calendar.monthrange(month.year, month.month)[1]
        # las_month_date = date(month.year, month.month, last_month_day)
        horario_by_week = []
        assistance_by_week = []
        
        conn = await DbManager.get_db_connection()
        async with conn.cursor() as cursor:
            query = "EXEC sp_ObtenerEmpleadoKeyId ?"
            await cursor.execute(query, cedula)
            row = await cursor.fetchone()
            if row:
                Empleado_id = row[0]
            else:
                return AssistanceReport()
            query = "EXEC sp_ObtenerHorarioMensual ?, ?, ?"
            params = (int(Empleado_id), month, last_month_date)
            await cursor.execute(query, params)
            rows = await cursor.fetchall()
            if rows:
                if len(rows) == 4:
                    for row in rows:
                        week = WorkingHours(Horas_lunes=row[0], Horas_martes=row[1], Horas_miercoles=row[2], Horas_jueves=row[3], Horas_viernes=row[4])
                        horario_by_week.append(week)
            query = "EXEC sp_ObtenerAsistenciaMensual ?, ?, ?"
            await cursor.execute(query, params)
            rows = await cursor.fetchall()
            if rows:
                if len(rows) == 4:
                    for row in rows:
                        week_assistance = WorkingHours(Horas_lunes=row[0], Horas_martes=row[1], Horas_miercoles=row[2], Horas_jueves=row[3], Horas_viernes=row[4])
                        assistance_by_week.append(week_assistance)
            for i in range(4):
                horario_week: WorkingHours = horario_by_week[i]
                assistance_week: WorkingHours = assistance_by_week[i]
                horario_week_days = array('i',[horario_week.Horas_lunes, horario_week.Horas_martes, horario_week.Horas_miercoles, horario_week.Horas_jueves, horario_week.Horas_viernes])
                assistance_week_days = array('i',[assistance_week.Horas_lunes, assistance_week.Horas_martes, assistance_week.Horas_miercoles, assistance_week.Horas_jueves, assistance_week.Horas_viernes])
                for i in range(5):
                    if horario_week_days[i] > assistance_week_days[i]:
                        if assistance_week_days[i] == 0:
                            assistance_report.Missed_days+=1
                        else:
                            missed_hours = horario_week_days[i] - assistance_week_days[i]
                            assistance_report.Missed_hours+=missed_hours
                            assistance_report.Normal_hours+= assistance_week_days[i]
                        
                    elif horario_week_days[i] < assistance_week_days[i]:
                        extra_hours = assistance_week_days[i]-horario_week_days[i]
                        assistance_report.Extra_hours+= extra_hours
                        assistance_report.Normal_hours+= horario_week_days[i]
                        
                    else:
                        assistance_report.Normal_hours+= assistance_week_days[i]
                    assistance_report.Total_hours+= assistance_week_days[i]
            print(assistance_report)
            return assistance_report
    except Exception as e:
        print(e)
        return AssistanceReport()
    finally:
        await conn.close()
