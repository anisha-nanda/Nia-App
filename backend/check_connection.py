import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

DB_URL = os.getenv("DATABASE_URL")

try:
    conn = psycopg2.connect(DB_URL)
    print("✅ Connected to Supabase PostgreSQL!")
    conn.close()
except Exception as e:
    print(f"❌ Connection failed: {e}")
