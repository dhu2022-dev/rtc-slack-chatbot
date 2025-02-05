from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from backend.bot.nlp.inference import get_intent, generate_response
from backend.bot.nlp.preprocess import extract_entities
from backend.database.database import get_db_connection, store_message

# Initialize Slack client
slack_client = WebClient(token="your-slack-bot-token")

def send_message(channel_id, text):
    try:
        # Step 1: Send message to Slack
        response = slack_client.chat_postMessage(channel=channel_id, text=text)
        print(f"Message sent: {response['message']['text']}")

        # Step 2: Process the message
        intent = get_intent(text)  # Get intent from BERT model
        entities = extract_entities(text)  # Extract entities using SpaCy & regex

        # Step 3: Store message with intent & entities in the database
        store_message("bot", text, intent, entities)  # Store in Postgres

    except SlackApiError as e:
        print(f"Error sending message: {e.response['error']}")


def handle_slack_message(user_id: str, message: str, channel_id: str):
    """
    Processes incoming Slack messages, extracts intent & entities, stores them,
    generates a response, and sends it back to Slack.
    """
    # Step 1: Process incoming message
    intent = get_intent(message)  # Classify intent using BERT
    entities = extract_entities(message)  # Extract important details

    # Step 2: Store the message in Postgres
    store_message(user_id, message, intent, entities)

    # Step 3: Generate a response from RTC GPT API
    response_text = generate_response(intent, entities)

    # Step 4: Send the response to Slack
    send_message(channel_id, response_text)
