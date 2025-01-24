# Main application entry point
import app.database as db
from tests.test_database import test_db_connection


def main():
    test_db_connection()
    # setting up database
    db.create_table()
    # test writing to database
    db.write_table()

    # test reading from database getting just user is testing
    db.read_table()
    # sending test message
    # send_message(channel_id="T088KLH1DFX", text="emily testing :,)")

if __name__ == "__main__":
    main()
