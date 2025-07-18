from fastapi import APIRouter, HTTPException
from db import get_db
from utils.mappings import ROLE_TABLES
from authen import hash_password, verify_password, create_token
from .schemas import AuthRequest  # your Pydantic model

router = APIRouter()

@router.post("/register/{role}")
def register(role: str, group: str, body: AuthRequest):
    if role not in ROLE_TABLES :
        raise HTTPException(400, "Invalid role or group")
    
    table = f"{group}_{role}s"

    if not body.name:
        raise HTTPException(400, "Name required for registration")

    conn, cur = get_db(), None
    try:
        cur = conn.cursor()

        # Check phone uniqueness across all three tables of the same role
        for t in ROLE_TABLES[role]:
            cur.execute(f"SELECT id FROM {t} WHERE phone = %s", (body.phone,))
            if cur.fetchone():
                raise HTTPException(400, f"Phone already registered in {t}")

        hashed = hash_password(body.password)

        cur.execute(
            f"INSERT INTO {table} (name, phone, password) VALUES (%s, %s, %s)",
            (body.name, body.phone, hashed)
        )

        conn.commit()
        return {"message": f"{role.capitalize()} registered in {table}"}

    finally:
        if cur: cur.close()
        conn.close()


@router.post("/login/{role}")
def login(role: str, body: AuthRequest):
    if role not in ROLE_TABLES:
        raise HTTPException(400, "Invalid role")

    conn, cur = get_db(), None
    try:
        cur = conn.cursor()
        for table in ROLE_TABLES[role]:
            cur.execute(f"SELECT id, name, password FROM {table} WHERE phone = %s", (body.phone,))
            row = cur.fetchone()
            if row:
                user_id, name, hashed = row
                if not verify_password(body.password, hashed):
                    raise HTTPException(401, "Incorrect password")

                token = create_token({
                    "user_id": str(user_id),
                    "role": role,
                    "table": table
                })

                return {
                    "message": f"Login successful as {role} in {table}",
                    "token": token,
                    "name": name,
                    "role": role,
                    "table": table
                }

        raise HTTPException(404, f"{role.capitalize()} not found")

    finally:
        if cur: cur.close()
        conn.close()
