from openai import OpenAI
from config import OPENAI_API_KEY


def generate_medical_report(demographics, medical_history, chat_transcript):
    YOUR_API_KEY = OPENAI_API_KEY

    # Construct prompt based on provided information
    prompt = (
        f"Summarize the following patient details into a concise medical report for the doctor:\n\n"
        f"Demographics:\n{demographics}\n\n"
        f"Medical History:\n{medical_history}\n\n"
        f"Chat Transcript:\n{chat_transcript}\n\n"
        "Provide a brief and relevant report including key information from the chat."
    )

    # Define messages with system role for context and user role for the task prompt
    messages = [
        {
            "role": "system",
            "content": (
                "You are a medical assistant. Based on the following patient information, "
                "provide a clear, accurate, and concise medical report for the doctor."
            ),
        },
        {
            "role": "user",
            "content": prompt,
        },
    ]

    # Initialize the OpenAI client
    client = OpenAI(api_key=YOUR_API_KEY)

    # Call the chat completion API to get the response
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"
