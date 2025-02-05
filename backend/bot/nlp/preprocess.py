# File that preprocesses input text

import spacy
import re

nlp = spacy.load("en_core_web_sm")

def extract_entities(text: str) -> dict:
    doc = nlp(text)
    entities = {ent.label_: ent.text for ent in doc.ents}

    # Custom regex-based extraction
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    emails = re.findall(email_pattern, text)
    if emails:
        entities["EMAIL"] = emails[0]

    return entities
