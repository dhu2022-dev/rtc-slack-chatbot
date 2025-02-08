import logging
from backend import SchemaManager, DataCRUD, S3Manager, SlackProcessor

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def main():
    # Configuration
    bucket_name = "rtc-slack-exports"
    directory_prefix = "member-support/"  # Replace with your S3 directory prefix

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

    # 2. List all Slack JSON files in S3
    logging.info(f"Listing all Slack JSON files in S3 under '{directory_prefix}'...")
    json_files = s3_handler.list_files_in_directory(directory_prefix)
    logging.info(f"Found {len(json_files)} JSON files in '{directory_prefix}'.")

    for slack_file_key in json_files:
        logging.info(f"Processing file: {slack_file_key}...")
        
        # 3. Load Slack JSON Export from S3
        raw_data = s3_handler.read_json_from_s3(slack_file_key)
        logging.info(f"Loaded {len(raw_data)} messages from {slack_file_key}.")

        # 4. Parse Slack JSON
        parsed_messages = slack_processor.extract_relevant_messages(raw_data)
        logging.info(f"Parsed {len(parsed_messages)} messages from {slack_file_key}.")

        # 5. Store Parsed Data in Database
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
        logging.info(f"Stored messages from {slack_file_key} in the database.")

if __name__ == "__main__":
    main()
