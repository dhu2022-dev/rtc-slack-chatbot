# Database connection functions

import psycopg2

def get_db_connection():
    connection = psycopg2.connect(
        host="your-db-host",
        database="your-db",
        user="your-user",
        password="your-password"
    )
    return connection

def create_table():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id SERIAL PRIMARY KEY,
        user_id VARCHAR(50),
        message_text TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    connection.commit()
    connection.close()
