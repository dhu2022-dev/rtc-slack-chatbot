import torch
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from datasets import load_dataset, Dataset

# Load and preprocess RTC-specific dataset
rtc_data = [
    {"text": "How do I prepare for an RTC technical interview?", "label": 0},
    {"text": "What events are happening this week?", "label": 1},
    {"text": "How do I join a mentorship program?", "label": 2},
    {"text": "Can I get a resume review?", "label": 3}
]
labels = ["interview_prep", "event_inquiry", "mentorship_signup", "resume_review"]

dataset = Dataset.from_list(rtc_data)

# Load tokenizer and model
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=len(labels))

# Tokenize dataset
def tokenize(batch):
    return tokenizer(batch["text"], padding=True, truncation=True)

dataset = dataset.map(tokenize, batched=True)

# Define training arguments
training_args = TrainingArguments(
    output_dir="./rtc_finetuned_intent_model",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    num_train_epochs=3,
    weight_decay=0.01,
    logging_dir="./logs",
)

# Train the model
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    tokenizer=tokenizer
)

trainer.train()

# Save the fine-tuned model
model.save_pretrained("rtc_finetuned_intent_model")
tokenizer.save_pretrained("rtc_finetuned_intent_model")
