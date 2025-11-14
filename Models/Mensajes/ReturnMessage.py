from pydantic import BaseModel
from typing import Optional

class ReturnMessage(BaseModel):
    state: Optional[bool] = None
    response_message: Optional[str] = None
