# Tests for database logic

from backend.database.schema_manager import get_db_connection

def test_db_connection():
    conn = get_db_connection()
    print(conn)
    assert conn is not None

