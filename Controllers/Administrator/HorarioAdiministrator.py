from fastapi import FastAPI, APIRouter, HTTPException
from Managers.db_manager import DbManager
from Models.Empleados.EmpleadosModel import Empleado
from Models.Horarios import TemporadaModel, HorarioModel
from Models.Mensajes.ReturnMessage import ReturnMessage
from Controllers.Administrator.EmpleadoAdministrator import obtener_empleado
from datetime import date, timedelta

router = APIRouter(prefix="/admin/horario", tags=["Administración de horarios"])

# Temporadas

@router.post("/ingresar-temporada")
async def ingresar_temporada(body: TemporadaModel.Temporada):
    conn = await DbManager.get_db_connection()

    try:
        async with conn.cursor() as cursor:
            query = "EXEC sp_CrearTemporada ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?"
            params = (body.nombre, body.fecha_inicio, body.fecha_final, body.mult_staff, body.mult_manager, body.mult_supervisor, body.mult_as, body.mult_foods, body.mult_rides, body.mult_games, body.mult_hk, body.mult_lifeguard, body.mult_maintainance)
            await cursor.execute(query, params)
            row = await cursor.fetchone()
            if row:
                sp_return = row[0]
                if sp_return == 0:
                    return ReturnMessage(state=True, response_message="Temporada creada con exito")
                if sp_return == 1:
                    return ReturnMessage(state=False, response_message="No es posible ingresar temporada dentro de estas fechas")
                if sp_return == 2:
                    return ReturnMessage(state=False, response_message="Error en las fechas de la temporada")
            else:
                return False
    except Exception as e:
        return ReturnMessage(state=False, response_message=str(e))
    finally:
        conn.close()
        
@router.post("/eliminar-temporada")
async def eliminar_temporada(temporada: str):
    conn = await DbManager.get_db_connection()
    
    try:
        async with conn.cursor() as cursor:
            query = "EXEC sp_EliminarTemporada ?"
            await cursor.execute(query, temporada)
            row = await cursor.fetchone()
            if row:
                sp_return = row[0]
                if sp_return == 0:
                    return ReturnMessage(state=True, response_message= "Temporada eliminada con exito")
                else:
                    return ReturnMessage(state=False, response_message= "La temporada seleccionada no existe")
    except Exception as e:
        return ReturnMessage(state=False, response_message=str(e))
    finally:
        conn.close()
        
@router.post("/obtener-temporadas")
async def obtener_temporadas(temporada: str):
    conn = await DbManager.get_db_connection()
    try:
        async with conn.cursor() as cursor:
            query = "EXEC sp_ObtenerTemporadaId ?"
            await cursor.execute(query, temporada)
            row = await cursor.fetchone()
            if row:
                temporada_id = row[0]
            else:
                return ReturnMessage(state=False, response_message="No existe una temporada con el nombre proporcionado")
            query = "EXEC sp_ObtenerTemporadas ?"
            await cursor.execute(query, int(temporada_id))
            row = await cursor.fetchone()
            if row:
                return TemporadaModel.Temporada( nombre=row[0], fecha_inicio=row[1], fecha_final=row[2], mult_staff=row[3], mult_manager=row[4], mult_supervisor=row[5], mult_as=row[6], mult_foods=row[7], mult_games=row[8], mult_hk=row[9], mult_rides=row[10], mult_maintainance=row[11], mult_lifeguard=row[12])
            else:
                return ReturnMessage(state=False, response_message="Error al obtener temporada")
    except Exception as e:
        return ReturnMessage(state=False, response_message=str(e))
    finally:
        conn.close

# Horarios

@router.post("/asignar-horario")
async def asignar_horario(body: HorarioModel.HorarioRequest):
    
    if body.Fecha_inicio.weekday() != 0:
        return ReturnMessage(state=False, response_message="Fecha de inicio invalida, el horario semanal debe comenzar en un lunes")
    fecha_final = body.Fecha_inicio + timedelta(days=4)
    conn = await DbManager.get_db_connection()
    try:
        async with conn.cursor() as cursor:
            query = "EXEC sp_ObtenerEmpleadoKeyId ?"
            await cursor.execute(query, body.Cedula_emplado)
            row = await cursor.fetchone()
            if row:
                key_id = row[0]
            else:
                return ReturnMessage(state=False, response_message="No existe un empleado con la cedula proporcionada")
            
            query = "EXEC sp_AsignarHorario ?, ?, ?, ?, ?, ?, ?, ?"
            params = (body.Fecha_inicio, fecha_final, key_id, body.Horas_lunes, body.Horas_martes, body.Horas_miercoles, body.Horas_jueves, body.Horas_viernes)
            await cursor.execute(query, params)
            row = await cursor.fetchone()
            if row:
                sp_response = row[0]
                if sp_response == 0:
                    return ReturnMessage(state=True, response_message="Horario asignado con exito")
                else:
                    return ReturnMessage(state=False, response_message="Ya existe un horario asignado para este empleado en la semana seleccionada")
            else:
                return ReturnMessage(state=False, response_message="Error al ejecutar stored procedure")
    except Exception as e:
        return ReturnMessage(state=False, response_message=str(e))
    finally:
        conn.close()
        
@router.post("/cancelar-horario")
async def cancelar_horario(body: HorarioModel.HorarioRequest):
    if body.Fecha_inicio.weekday() != 0:
        return ReturnMessage(state=False, response_message="Fecha de inicio invalida, el horario semanal debe comenzar en un lunes")
    conn = await DbManager.get_db_connection()
    try:
        async with conn.cursor() as cursor:
            query = "EXEC sp_ObtenerEmpleadoKeyId ?"
            await cursor.execute(query, body.Cedula_emplado)
            row = await cursor.fetchone()
            if row:
                key_id = row[0]
            else:
                return ReturnMessage(state=False, response_message="No existe un empleado con la cedula proporcionada")
            query = "EXEC sp_EliminarHorario ?, ?"
            params = (key_id, body.Fecha_inicio)
            await cursor.execute(query, params)
            row = await cursor.fetchone()
            if row:
                sp_response = row[0]
                if sp_response == 0:
                    return ReturnMessage(state=True, response_message="Horario eliminado con exito")
                else:
                    return ReturnMessage(state=False, response_message="No existe un horario asignado para este empleado en esta fecha")
            else:
                return ReturnMessage(state=False, response_message="Error al ejecutar stored procedure")
    except Exception as e:
        return ReturnMessage(state=False, response_message=str(e))
    finally:
        conn.close()
        
@router.post("/obtener-horario")
async def obtener_horario(body: HorarioModel.HorarioRequest):
    conn = await DbManager.get_db_connection()
    
    try:
        async with conn.cursor() as cursor:
            query = "EXEC sp_ObtenerHorario ?, ?"
            params = (body.Cedula_emplado, body.Fecha_inicio)
            await cursor.execute(query, params)
            row = await cursor.fetchone()
            if row:
                return HorarioModel.Horario(Nombre_empleado=row[0], Apellido_empleado=row[1],
                                            Fecha_inicio=row[2], Fecha_final=row[3],
                                            Horas_lunes=row[4], Horas_martes=row[5],
                                            Horas_miercoles=row[6], Horas_jueves=row[7], Horas_viernes=row[8])
            else: 
                return ReturnMessage(state=False, response_message="No existe un horario en esta fecha asignado a este empleado")
    except Exception as e:
        return ReturnMessage(state=False, response_message=str(e))
    finally:
        conn.close()
        