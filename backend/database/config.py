# Configurations

import os

DATABASE_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD")
}

SLACK_CONFIG = {
    "token": os.getenv("SLACK_TOKEN"),
    "signing_secret": os.getenv("SLACK_SIGNING_SECRET")
}
