# File for NLP model inference
from transformers import BertTokenizer, BertForSequenceClassification
from sentence_transformers import SentenceTransformer
import chromadb
import requests

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertForSequenceClassification.from_pretrained("bert_intent_model")
embedding_model = SentenceTransformer("bert-base-uncased")

chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection("intent_embeddings")

def get_intent(message: str) -> str:
    tokens = tokenizer(message, return_tensors="pt", truncation=True)
    output = model(**tokens)
    intent = output.logits.argmax().item()  # Get predicted intent class
    return intent

def generate_response(intent: str, entities: dict) -> str:
    url = "https://your-rtc-gpt-api.com/generate"
    headers = {"Authorization": "Bearer YOUR_API_KEY"}

    payload = {
        "intent": intent,
        "entities": entities
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json().get("response", "Sorry, I don't understand.")
