from datetime import date
from Managers.db_manager import DbManager
from Models.Core.AssistanceModel import WorkingHours, AssistanceReport
import calendar

async def CalculateAssistance(month: date, cedula: str):
    try:
        last_month_day = calendar.monthrange(month.year, month.month)[1]
        las_month_date = date(month.year, month.month, last_month_day)
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
                return
            query = "EXEC sp_ObtenerHorarioMensual ?, ?, ?"
            params = (int(Empleado_id), month, las_month_date)
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
                print("lol")
    except Exception as e:
        print(e)
        return
    finally:
        await conn.close()