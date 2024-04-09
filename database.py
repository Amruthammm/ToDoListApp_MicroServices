# database.py

import pymysql
from sqlalchemy import create_engine
from models import db

# Function to create the database connection
def create_connection():
    try:
        # Establish the database connection
        conn = pymysql.connect(
            host='todo.ckgbjrurodq3.ap-south-1.rds.amazonaws.com',
            port=3306,
            user='admin',
            password='todo-admin',
            database='to_do_app'
        )

        # Construct connection string
        conn_str = f"mysql+pymysql://{conn.user}:{conn.password}@{conn.host}:{conn.port}/{conn.db}"

        # Return SQLAlchemy engine
        return create_engine(conn_str)
    except Exception as e:
        print("Error connecting to database:", e)
        return None
