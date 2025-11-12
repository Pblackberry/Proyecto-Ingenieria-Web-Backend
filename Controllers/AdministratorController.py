from fastapi import FastAPI, APIRouter, HTTPException
from Managers.db_manager import DbManager
from Models.Empleados.EmpleadosModel import Empleado
from Managers.CedulaManager import comprobarCedula

router = APIRouter(prefix="/admin", tags=["Administrador"])

# Administracion de empleados

@router.post("/ingresar-empleado")
async def ingresar_empleado(body: Empleado):
    conn = await DbManager.get_db_connection()
    try:
        print(body.Cedula)
        flag = comprobarCedula(body.Cedula)
        print(f"flag: {flag}")
        if not flag:
            print("entro")
            return False
        async with conn.cursor() as cursor:
            cargo_pk_query = "EXEC sp_ObtenerCargoKeyId ?"
            await cursor.execute(cargo_pk_query, body.Cargo)
            row = await cursor.fetchone()
            if row:
                print("entro cargo")
                cargo_keyid = row[0]
            else:
                return False
            area_pk_query = "EXEC sp_ObtenerAreaKeyId ?"
            await cursor.execute(area_pk_query, body.Area)
            row = await cursor.fetchone()
            if row:
                print("entro area")
                area_keyid = row[0]
            else:
                return False
            query = "EXEC sp_InsertarEmpleado ?, ?, ?, ?, ?"
            params = (body.Nombre, body.Apellido, body.Cedula, cargo_keyid, area_keyid)
            await cursor.execute(query, params)
        conn.close()
        return True
    except Exception:
        return False

@router.post("/obtener-empleado")
async def obtener_empleado(cedula: str):
    conn = await DbManager.get_db_connection()
    try:
        async with conn.cursor() as cursor:
            query = "EXEC sp_ObtenerEmpleado ?"
            params = (cedula)
            await cursor.execute(query, params)
            row = await cursor.fetchone()
            if row:
                empleado =  Empleado(Nombre=row[1], Apellido=row[2], Cedula=row[3], Area=row[4], Cargo=row[5])
                return empleado
            else:
                return None
    finally:
        await conn.close()
    
@router.get("/obtener-empleados")
async def obtener_empleados_all():
    conn = await DbManager.get_db_connection()
    try:
        async with conn.cursor() as cursor:
            query = "EXEC sp_ObtenerEmpleadosAll"
            await cursor.execute(query)
            rows = await cursor.fetchall()
            if rows:
                
                columns = [column[0] for column in cursor.description]
                data = [dict(zip(columns, row)) for row in rows]
                return data
            else:
                return None 
    finally:
        await conn.close()
        
@router.post("/eliminar-empleados")
async def eliminar_empleado(cedula: str):
    conn = await DbManager.get_db_connection()
    try:
        async with conn.cursor() as cursor:
            query = "EXEC sp_EliminarEmpleado ?"
            await cursor.execute(query, cedula)
            return True
    except Exception:
        return False
        
