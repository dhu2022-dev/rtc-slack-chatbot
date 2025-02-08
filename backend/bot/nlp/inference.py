import logging
from transformers import BertTokenizer, BertForSequenceClassification
from sentence_transformers import SentenceTransformer
from bertopic import BERTopic
import chromadb
import spacy
import torch
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load BERT-based intent classification model
logging.info("Loading BERT tokenizer and model for intent classification...")
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertForSequenceClassification.from_pretrained("rtc_finetuned_intent_model")

# Load BERTopic model for topic clustering
logging.info("Initializing BERTopic model...")
topic_model = BERTopic().load("rtc_bertopic_model")

# Load Sentence Transformer for embeddings
logging.info("Loading SentenceTransformer for embedding generation...")
embedding_model = SentenceTransformer("bert-base-uncased")

# Load spaCy Named Entity Recognition model
logging.info("Loading spaCy NER model...")
nlp = spacy.load("en_core_web_trf")

# Set up ChromaDB client
logging.info("Initializing ChromaDB client...")
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection("intent_embeddings")

def get_intent(message: str) -> str:
    """Classify user intent using BERT intent classification."""
    logging.info(f"Tokenizing input message: {message}")
    tokens = tokenizer(message, return_tensors="pt", truncation=True)
    
    logging.info("Performing intent classification...")
    output = model(**tokens)
    intent = output.logits.argmax().item()
    logging.info(f"Predicted intent: {intent}")
    
    return str(intent)  # Convert intent class to string label

def get_topic(messages: list) -> list:
    """Use trained BERTopic model for RTC queries."""
    logging.info("Performing RTC topic modeling...")
    topics, _ = topic_model.transform(messages)
    logging.info(f"Identified RTC topics: {topics}")
    return topics

def extract_entities(message: str) -> dict:
    """Extract entities from user messages using spaCy NER."""
    logging.info(f"Extracting entities from message: {message}")
    doc = nlp(message)
    entities = {ent.label_: ent.text for ent in doc.ents}
    logging.info(f"Extracted entities: {entities}")
    return entities

def store_embedding(message: str, intent: str):
    """Store message embeddings in ChromaDB."""
    logging.info(f"Generating embedding for message: {message}")
    embedding = embedding_model.encode(message).tolist()
    
    logging.info("Storing embedding in ChromaDB...")
    collection.add(
        documents=[message],
        metadatas=[{"intent": intent}],
        embeddings=[embedding]
    )
    logging.info("Embedding stored successfully.")

def retrieve_embedding(message: str) -> str:
    """Retrieve the most similar stored intent from ChromaDB."""
    logging.info(f"Retrieving the closest stored intent for message: {message}")
    embedding = embedding_model.encode(message)
    results = collection.query(query_embeddings=[embedding], n_results=1)
    if results and results["documents"]:
        logging.info(f"Closest match found: {results['documents'][0]}")
        return results["documents"][0]  # Return closest stored message
    logging.info("No close match found.")
    return ""

if __name__ == "__main__":
    test_message = "How do I prepare for a technical interview?"
    logging.info("Starting inference pipeline...")
    
    intent = get_intent(test_message)
    entities = extract_entities(test_message)
    
    logging.info("Storing intent and message embedding...")
    store_embedding(test_message, intent)
    
    similar_intent = retrieve_embedding(test_message)
    logging.info(f"Final Output - Intent: {intent}, Entities: {entities}, Similar Intent: {similar_intent}")
