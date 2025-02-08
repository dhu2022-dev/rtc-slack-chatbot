import re

class SlackProcessor:
    def __init__(self):
        pass

    def extract_relevant_messages(self, slack_data):
        """Extract relevant messages from Slack export."""
        messages = []
        
        for entry in slack_data:
            # Ignore empty messages or system-generated messages
            if "text" not in entry or (not entry["text"].strip() and "files" not in entry):
                continue

            # Extract relevant fields
            message_data = {
                "text": self._normalize_text(entry["text"]),
                "thread_ts": entry.get("thread_ts"),
                "user": entry.get("user"),
                "user_name": entry.get("user_profile", {}).get("real_name", "Unknown"),
                "ts": entry.get("ts"),
                "replies": entry.get("replies", []),
            }

            messages.append(message_data)

        return messages

    @staticmethod
    def _normalize_text(text):
        """Normalize text by removing URLs and extra whitespace, and converting to lowercase."""
        text = re.sub(r"http\S+", "", text.strip().lower())  # Remove URLs
        text = re.sub(r"\s+", " ", text)  # Collapse multiple spaces
        return text
