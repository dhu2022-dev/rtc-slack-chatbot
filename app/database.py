import psycopg2
import os
from dotenv import load_dotenv

load_dotenv() # have to load env before calling

def get_db_connection():
    connection = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
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

def write_table():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO messages (user_id, message_text)
        VALUES ('testing', 'This is a test message');
    """)
    connection.commit()
    connection.close()

def read_table():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT * FROM messages WHERE user_id = 'testing';
    """)

    testing_records = cursor.fetchall()
    print(testing_records)
    connection.commit()
    connection.close()
