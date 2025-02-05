import psycopg2
import os
import re
from backend.database.database import get_db_connection  # Ensure connection function is imported


def fetch_relevant_message(query: str) -> str:
    """
    Searches past messages in the database and returns the most relevant one.
    """
    connection = get_db_connection()
    cursor = connection.cursor()

    # Extract keywords (simple regex-based keyword search)
    keywords = re.findall(r'\b\w+\b', query.lower())

    # If there are no keywords, return nothing
    if not keywords:
        return "I couldn't find anything relevant."

    # Build SQL query to search past messages
    sql_query = f"""
        SELECT message_text FROM messages
        WHERE {' OR '.join([f"message_text ILIKE '%{kw}%'" for kw in keywords])}
        ORDER BY timestamp DESC LIMIT 1;
    """

    cursor.execute(sql_query)
    result = cursor.fetchone()
    connection.close()

    if result:
        return result[0]  # Return the most relevant message
    else:
        return "I couldn't find anything relevant."

