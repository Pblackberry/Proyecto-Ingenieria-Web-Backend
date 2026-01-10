import logging
from fastapi import FastAPI, APIRouter, HTTPException, Response
from Managers.db_manager import DbManager
from Managers.db_manager import DbLoginService
from Models.LoginModels import UserData
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt


router = APIRouter(prefix="/login", tags=["Login"])
SECRET_KEY = "tu-super-secreto-que-nadie-debe-saber"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Crea un JSON Web Token (JWT) de acceso.
    
    :param data: El payload que contendrá el token (ej. {"sub": "nombre_usuario"}).
    :param expires_delta: Objeto timedelta opcional que especifica la duración del token.
    :return: El JWT codificado (una cadena de texto).
    """
    to_encode = data.copy()
    
    # 1. Calcular la expiración (exp)
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # Por defecto, expira en 15 minutos si no se especifica
        expire = datetime.utcnow() + timedelta(minutes=15)
        
    # Añadir la marca de tiempo de expiración al payload
    to_encode.update({"exp": expire})
    
    # 2. Codificar y firmar el Token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

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
        user = await DbLoginService.try_get_user(body.email)
        if user is not None:
            return user
        else:
            return UserData(username=None, email=None, password=None)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    
@router.post("/update-user")
async def update_user(body: UserData):
    try:
        user = await DbLoginService.try_get_user(body.email)
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
        user = await DbLoginService.try_get_user(body.email)
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