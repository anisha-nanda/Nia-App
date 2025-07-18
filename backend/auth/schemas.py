# auth/schemas.py
from pydantic import BaseModel, EmailStr

class AuthRequest(BaseModel):
    email: str
    id:str
    password: str
