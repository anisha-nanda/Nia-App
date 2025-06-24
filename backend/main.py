# backend/main.py

import psycopg2
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Fetch the full connection URL from environment variable
DB_URL = os.getenv("DATABASE_URL")

# Connect to the database
try:
    connection = psycopg2.connect(DB_URL)
    print("Connection to Supabase PostgreSQL successful!")

    # Create a cursor to execute SQL queries
    cursor = connection.cursor()

    # Example query to check connection
    cursor.execute("SELECT NOW();")
    result = cursor.fetchone()
    print("Current Time from DB:", result)

    # Clean up
    cursor.close()
    connection.close()
    print(" Connection closed.")

except Exception as e:
    print(f"Failed to connect: {e}")
