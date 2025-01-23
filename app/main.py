# Main application entry point
from app.database import create_table
from app.bot import send_message

def main():
    # setting up database
    create_table()

    # sending test message
    send_message(channel_id="T088KLH1DFX", text="emily testing :,)")

if __name__ == "__main__":
    main()
