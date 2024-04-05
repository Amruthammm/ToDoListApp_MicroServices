# database.py

import pyodbc

# Define the connection string
conn_str = (
    'DRIVER={SQL Server};'
    'SERVER=TEJU\\SQLEXPRESS;'
    'DATABASE=HRMS_DB;'
    'Trusted_Connection=yes;'
)

# Function to create the database connection
def create_connection():
    try:
        # Establish the database connection
        conn = pyodbc.connect(conn_str)
        return conn
    except Exception as e:
        print("Error connecting to database:", e)
        return None
