# model_api.py
import os
from groq import Groq

# Initialize the Groq client with the API key from environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not set in environment.")
client = Groq(api_key=GROQ_API_KEY)

def generate_text(messages: list, model_name: str) -> str:
    """
    Helper function to call the Groq chat completion API.
    `messages` should be a list of dicts with 'role' and 'content'.
    Returns the assistant's content as a string.
    """
    completion = client.chat.completions.create(messages=messages, model=model_name)
    # Extract the generated text from the first choice
    return completion.choices[0].message.content
