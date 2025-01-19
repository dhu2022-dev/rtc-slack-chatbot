# Slack bot logic

import slack_sdk

def slack_event_handler(event_data):
    # Process the Slack event (e.g., message, reaction)
    event_type = event_data.get('type')
    if event_type == "message":
        return "Hello, World!"  # Respond to messages
