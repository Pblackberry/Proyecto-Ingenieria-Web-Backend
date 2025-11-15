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
            query = "EXEC sp_CrearTemporada ?, ?, ?, ?"
            params = (body.nombre, body.fecha_inicio, body.fecha_final, body.multiplicador)
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
        
@router.get("/obtener-temporadas")
async def obtener_temporadas():
    conn = await DbManager.get_db_connection()
    try:
        async with conn.cursor() as cursor:
            query = "EXEC sp_ObtenerTemporadas"
            await cursor.execute(query)
            rows = await cursor.fetchall()
            if rows:
                columns = [column[0] for column in cursor.description]
                data = [dict(zip(columns, row)) for row in rows]
                return data
            else:
                return ReturnMessage(state=False, response_message="No hay temporadas registradas")
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