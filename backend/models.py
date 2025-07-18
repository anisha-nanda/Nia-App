#register page input and login page input

from pydantic import BaseModel



class reg_users(BaseModel):

    name: str
    id:str
    phone: int
    location:str
    password: str

class login_users(BaseModel):

    name: str
    id:str
    password: str    


class login_sellers(BaseModel): 
    name:str
    seller_id:str
    password:str   
    phone:int

class reg_sellers(BaseModel): 
    name:str
    seller_id:str
    password:str
    location:str   
       



