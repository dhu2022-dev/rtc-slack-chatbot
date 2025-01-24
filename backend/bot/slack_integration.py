from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from backend.database.database import get_db_connection, create_table

# Initialize Slack client
slack_client = WebClient(token="your-slack-bot-token")

def send_message(channel_id, text):
    try:
        response = slack_client.chat_postMessage(channel=channel_id, text=text)
        print(f"Message sent: {response['message']['text']}")

        # Store message in the database
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO messages (user_id, message_text, timestamp)
            VALUES (%s, %s, %s)
        """, ("bot", text, response["ts"]))
        connection.commit()
        connection.close()
    except SlackApiError as e:
        print(f"Error sending message: {e.response['error']}")