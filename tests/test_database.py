# Tests for database logic

from app.database import get_db_connection

def test_db_connection():
    conn = get_db_connection()
    assert conn is not None
