import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Load model and tokenizer
model_name = "gpt2"  # or 'gpt2-medium' for a larger model
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# Function to generate responses
def generate_response(prompt):
    
    inputs = tokenizer.encode(prompt, return_tensors="pt")
    attention_mask = torch.ones(inputs.shape, dtype=torch.long)
    outputs = model.generate(
        inputs,
        max_length=100,         # Reasonable max length to control response size
        num_return_sequences=1, # Only one response
        temperature=1,        # Slightly lower for better consistency
        top_p=0.9,              # Limits sampling to top tokens, improving relevance
        pad_token_id=tokenizer.eos_token_id,
        do_sample=True,         # Enables sampling with temperature and top_p
        attention_mask=attention_mask  # Set attention mask to avoid warnings
    )
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Get the first line of the response
    first_line = response.split('\n')[0]
    return first_line

# Chat loop
print("ChatGPT: Hi! How can I help you today?")
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("ChatGPT: Goodbye!")
        break
    response = generate_response(user_input)
    print("ChatGPT:", response)