from bertopic import BERTopic

def train_topic_model(messages):
    """Train BERTopic on RTC-specific messages."""
    topic_model = BERTopic()
    topics, _ = topic_model.fit_transform(messages)
    
    # Save the model for reuse
    topic_model.save("rtc_bertopic_model")
    return topic_model

# Train the model
rtc_messages = [
    "What are the best coding resources?",
    "How do I get a mentor?",
    "Where can I find job interview prep guides?",
    "Any tips for resume building?",
    "How do I get involved in RTC events?"
]
topic_model = train_topic_model(rtc_messages)
