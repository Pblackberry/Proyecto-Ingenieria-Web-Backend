from pydantic import BaseModel, EmailStr
from typing import Optional

class UserData(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None