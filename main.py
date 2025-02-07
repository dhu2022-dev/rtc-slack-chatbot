import logging
from backend import SchemaManager, DataCRUD, ConnectionPool, S3Manager, SlackProcessor

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def main():
    # Configuration
    bucket_name = "rtc-slack-exports"
    slack_file_key = "member-support/2025-02-02.json"  # Replace with your S3 file path

    # Initialize components
    logging.info("Initializing components...")
    s3_handler = S3Manager(bucket_name)
    slack_processor = SlackProcessor()
    schema_manager = SchemaManager()
    data_access = DataCRUD()

    # 1. Create Database Tables
    logging.info("Setting up database tables...")
    schema_manager.create_tables()
    logging.info("Database tables created successfully.")

    # 2. Load Slack JSON Export from S3
    logging.info(f"Loading Slack JSON export from S3: {slack_file_key}...")
    raw_data = s3_handler.read_json_from_s3(slack_file_key)
    logging.info(f"Loaded {len(raw_data)} messages from S3.")

    # 3. Parse Slack JSON
    logging.info("Parsing Slack JSON data...")
    parsed_messages = slack_processor.extract_relevant_messages(raw_data)
    logging.info(f"Parsed {len(parsed_messages)} messages.")

    # 4. Store Parsed Data in Database
    logging.info("Storing parsed messages in the database...")
    for message in parsed_messages:
        data_access.store_message(
            user_id=message["user"],
            user_name=message["user_name"],
            message=message["text"],
            intent=None,  # Intent can be added later
            entities={},  # Entities can be added later
            ts=message["ts"],
            thread_ts=message["thread_ts"]
        )

if __name__ == "__main__":
    main()