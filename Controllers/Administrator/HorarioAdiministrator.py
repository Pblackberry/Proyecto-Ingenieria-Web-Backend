from fastapi import FastAPI, APIRouter, HTTPException
from Managers.db_manager import DbManager
from Models.Horarios.TemporadaModel import Temporada
from Models.Mensajes.ReturnMessage import ReturnMessage

router = APIRouter(prefix="/admin/horario", tags=["Administración de horarios"])

# Temporadas

@router.post("/ingresar-temporada")
async def ingresar_temporada(body: Temporada):
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
            