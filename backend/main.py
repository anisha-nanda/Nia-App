# backend/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from dotenv import load_dotenv
import os
from models import reg_sellers,reg_users,login_sellers,login_users
from authen import hash_password, verify_password, create_token
from db import get_db

from auth.routes import router as auth_router

app = FastAPI()

app.include_router(auth_router, prefix="/auth")
load_dotenv()



DB_URL = os.getenv("DATABASE_URL")
@app.get("/")
def read_root():
    return {"message": "Welcome to the API"}