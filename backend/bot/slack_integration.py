from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from backend.bot.nlp.preprocess.preprocess import fetch_relevant_message
from backend.database.schema_manager import store_message
import os

# Initialize Slack client
slack_client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))

def send_message(channel_id: str, text: str):
    """
    Sends a message to Slack and stores it in the database.
    """
    try:
        response = slack_client.chat_postMessage(channel=channel_id, text=text)
        print(f"Message sent: {response['message']['text']}")

        # Store the bot's response in the database
        store_message("bot", text, intent="bot_response", entities={})  # Mark it as a bot response

    except SlackApiError as e:
        print(f"Error sending message: {e.response['error']}")


def handle_slack_message(user_id: str, message: str, channel_id: str):
    """
    Searches past messages for relevant answers and sends the best match to Slack.
    """
    # Step 1: Search for a relevant past message
    relevant_message = fetch_relevant_message(message)

    # Step 2: Store the user's message in the database
    store_message(user_id, message, intent="faq_lookup", entities={})  # Mark it as an FAQ lookup

    # Step 3: Send the best-matching message to Slack
    send_message(channel_id, relevant_message)  # Use send_message() to store bot's response too
