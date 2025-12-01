from fastapi import FastAPI, APIRouter, HTTPException
from Managers.db_manager import DbManager
from Models.LoginModels import UserData
import logging


router = APIRouter(prefix="/login", tags=["Login"])

@router.post("/create-user")
async def insert_user(body: UserData):
    conn = await DbManager.get_db_connection()
    try:
        async with conn.cursor() as cursor:
            query = "EXEC sp_InsertUser ?, ?, ?"
            params = (body.username, body.email, body.password)
            await cursor.execute(query, params)
        conn.close()
        return {"message":"usuario insertado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    finally:
        await conn.close()
    
@router.post("/read-user")
async def read_user(body: UserData):
    try: 
        user = await DbManager.try_get_user(body)
        if user is not None:
            return user
        else:
            return UserData(username=None, email=None, password=None)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    
@router.post("/update-user")
async def update_user(body: UserData):
    try:
        user = await DbManager.try_get_user(body)
        if user is not None:
            db_connection = await DbManager.get_db_connection()
            async with db_connection.cursor() as cursor:
                query = "EXEC sp_EditUser ?, ?, ?"
                params = (body.email, body.username, body.password)
                await cursor.execute(query, params)
            db_connection.close()
            return True
        else:
            return UserData(username=None, email=None, password=None)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    
    
@router.post("/delete-user")
async def delete_user(body: UserData):
    try:
        user = await DbManager.try_get_user(body)
        if user is not None:
            db_connection = await DbManager.get_db_connection()
            async with db_connection.cursor() as cursor:
                query = "EXEC sp_DeleteUser ?, ?"
                params = (body.email, body.password)
                await cursor.execute(query, params)
            db_connection.close()
            return True
        else:
            return UserData(username=None, email=None, password=None)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e