import torch
from transformers import BertTokenizer, BertForSequenceClassification, pipeline

# Load pre-trained model and tokenizer for BERT
model_name = "bert-base-uncased"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name)

# Set up a text generation pipeline with GPT-2
# response_generator = pipeline("text-generation", model="gpt2")
response_generator = pipeline("text-generation", model="EleutherAI/gpt-neox-20b")

# Function to classify text
def classify_text(texts):
    inputs = tokenizer(texts, padding=True, truncation=True, return_tensors="pt", max_length=512)

    with torch.no_grad():
        outputs = model(**inputs)

    logits = outputs.logits
    predictions = torch.argmax(logits, dim=-1)

    return predictions

# Function to generate a serious AI response
def generate_serious_response(input_text):
    # Create a focused prompt to encourage serious responses
    serious_prompt = f"{input_text}"
    response = response_generator(serious_prompt, max_length=50, num_return_sequences=1, pad_token_id=tokenizer.eos_token_id)[0]['generated_text']
    
    # Filter out casual language by removing extra text
    serious_response = response.split("\n")[0].strip()  # Take the first line as the response
    return serious_response

# Main program loop
def main():
    def answer(user_input):
        # Generate a serious AI response based on the input text
        ai_response = generate_serious_response(user_input)

        print(f"AI Response: {ai_response}")

if __name__ == "__main__":
    main()
