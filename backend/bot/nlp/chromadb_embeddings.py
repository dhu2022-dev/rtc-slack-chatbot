from sklearn.datasets import fetch_20newsgroups #loading sample dataset
import chromadb
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
import logging 

# this code here will change when we load from the aws db
newsgroups = fetch_20newsgroups(subset='all')
newsgroups_data = newsgroups.data
newsgroups_labels = newsgroups.target

#load embeddings + initialize chromadb
logging.info("Loading the model")
embedding_model = SentenceTransformer("bert-base-uncased")
logging.info("generating embeddings")
embeddings = embedding_model.encode(newsgroups_data, show_progress_bar=True)

logging.info("Initializing ChromaDB client...")
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection("data_embeddings")

#storing in chromadb
for i, doc in enumerate(newsgroups_data):
    metadata = {
        "label": newsgroups_labels[i],
        "data": doc
    }

    collection.add(
        documents=[doc],
        metadatas=[metadata],
        embeddings=[embeddings[i].tolist()]
    )

# testing w/ a sample query
query = "What are the latest trends in deep learning?"
query_embedding = embedding_model.encode(query).tolist()
query_results = collection.query(query_embedding, k=5)

for result in query_results:
    print(result.metadata["data"])
    print(result.metadata["label"])
    print(result.embedding)
    print("\n")