import os
from slack_sdk import WebClient
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
env_path = Path('../../') / '.env'
load_dotenv(dotenv_path=env_path)

# Initialize Slack client
client = WebClient(token=os.getenv("SLACK_API_TOKEN"))

# Send a test message
response = client.chat_postMessage(channel="#test", text="What's good friends, it's David.")
print(response)
