import aioodbc
import asyncio
from Models.LoginModels import UserData
class DbManager:
    """Static class for dealing with database connections"""
    @staticmethod
    async def get_db_connection():
        """Establece y devuelve una conexion a la base de datos""" 
        name_server = 'LAPTOP-OJJP1HNK'
        database ='UWM'
        username ='administrator'
        password = 'LionelMessi'
        controlador_odbc='ODBC Driver 17 for SQL Server'
        connection_string = f'DRIVER={controlador_odbc};SERVER={name_server};DATABASE={database};UID={username};PWD={password}'
        conn = await aioodbc.connect(dsn=connection_string, autocommit=True)
        return conn
    
    @staticmethod
    async def try_get_user(body: UserData):
        conn = await DbManager.get_db_connection()
        try:
            async with conn.cursor() as cursor:
                query = "EXEC sp_SelectUser ?"
                await cursor.execute(query, (body.email))
                row = await cursor.fetchone()
                if row:
                    user =  UserData(username=row[0], email=row[1], password=None)
                    return user
                else:
                    return None
        finally:
            conn.close()
