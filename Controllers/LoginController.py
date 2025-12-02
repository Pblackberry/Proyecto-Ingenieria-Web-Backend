import logging
from fastapi import FastAPI, APIRouter, HTTPException, Response
from Managers.db_manager import DbManager
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
async def read_user(body: UserData, response: Response):
    """
    Verifica las credenciales, genera un JWT si es exitoso y lo establece en una cookie.
    """
    try:
        # 1. Verificar Credenciales
        # DbManager debe verificar el username/email y el password
        user = await DbManager.try_get_user(body)
        
        if user is None:
            # Es importante no dar detalles específicos de por qué falló
            raise HTTPException(
                status_code=401,
                detail="Credenciales de usuario o contraseña inválidas",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # 2. Generar el Token JWT
        # El contenido del token (payload) suele ser el ID o el username del usuario.
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, # 'sub' es la convención para Subject
            expires_delta=access_token_expires
        )

        # 3. Establecer el Token en una Cookie HTTP
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,       # La cookie no es accesible por JavaScript (seguridad XSS)
            samesite='Lax',      # Protección contra CSRF
            secure=True,         # Solo se envía a través de HTTPS (requiere que el servidor lo soporte)
            max_age=access_token_expires.total_seconds()
        )
        
        # 4. Retornar Respuesta Exitosa
        # Se puede retornar un mensaje de éxito o los datos del usuario (sin password).
        return {"message": "Inicio de sesión exitoso", "username": user.username}

    except HTTPException:
        # Volver a lanzar la excepción 401
        raise
    except Exception as e:
        # Manejo de otros errores (ej. base de datos)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from e
    # try: 
    #     user = await DbManager.try_get_user(body)
    #     if user is not None:
    #         return user
    #     else:
    #         return UserData(username=None, email=None, password=None)
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e)) from e
    
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