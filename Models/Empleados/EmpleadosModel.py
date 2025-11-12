from pydantic import BaseModel, EmailStr
from typing import Optional

class Empleado(BaseModel):
    Nombre: Optional[str] = None
    Apellido: Optional[str] = None
    Cedula: Optional[str] = None
    Area: Optional[str] = None
    Cargo: Optional[str] = None
    
# class GetEmpleadoRequest(BaseModel):
#     Nombre: Optional[str] = None
#     Apellido: Optional[str] = None
    
# class GetEmpleadoResponse(BaseModel):
#     Nombre: Optional[str] = None
#     Apellido: Optional[str] = None
#     Cedula
#     Area: Optional[str] = None
#     Cargo: Optional[str] = None
    