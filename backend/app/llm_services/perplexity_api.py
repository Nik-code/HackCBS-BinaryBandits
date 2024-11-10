from openai import OpenAI
from .config import PERPLEXITY_API_KEY


def get_medical_information(prompt):
    YOUR_API_KEY = PERPLEXITY_API_KEY

    # Define the initial system message to set context for medical information
    messages = [
        {
            "role": "system",
            "content": (
                "You are an artificial intelligence assistant specialized in "
                "providing accurate, detailed, and reliable medical information. "
                "Please respond with medically accurate and evidence-infebased answers "
                "to the best of your ability."
            ),
        },
        {
            "role": "user",
            "content": prompt,
        },
    ]

    # Initialize the client
    client = OpenAI(api_key=YOUR_API_KEY, base_url="https://api.perplexity.ai")

    # Call the chat completion API to get the response
    try:
        response = client.chat.completions.create(
            model="llama-3.1-sonar-large-128k-online",
            messages=messages,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"
