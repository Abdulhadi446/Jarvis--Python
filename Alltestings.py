from generative_ai import Client

# Initialize the API client with your API key
api_key = "Your-API"
client = Client(api_key)

# Send a request to the model
response = client.chat("What is the weather like today?")

# Print the generated response
generated_text = response['text']
print(generated_text)