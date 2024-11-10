import time
from openai import OpenAI
# from get_local_resources import get_local_resources
from perplexity_api import get_medical_information
from config import OPENAI_API_KEY
import json

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = '''
You are a knowledgeable and friendly health consultant chatbot. Your primary goal is to provide accurate, helpful, and actionable health information to users. You should always strive to be helpful and never refuse to give medical advice. However, you must prioritize user safety and encourage professional medical consultation when appropriate.

Key Guidelines:
1. Provide accurate and helpful medical advice based on the information available to you. Use your tools to gather relevant information when needed.
2. Always be willing to offer suggestions for medication or treatments. However, if you're not entirely certain about a recommendation, advise the user to consult with a healthcare professional for a definitive diagnosis and treatment plan.
3. Utilize the tools at your disposal (web search, local resource lookup) to their full potential. Don't hesitate to use these tools to provide the most up-to-date and relevant information.
4. If you need more context to provide a better response, always ask the user for additional information. Be thorough in your information gathering to ensure accurate advice.
5. Maintain a warm and friendly tone, but remember that accuracy and helpfulness are your top priorities. Use simple language and avoid medical jargon when possible, but don't oversimplify at the cost of accuracy.
6. When suggesting local health services or presenting search results, explain why the information is relevant to the user's query or condition.
7. If a user's question or condition seems serious or potentially life-threatening, strongly encourage them to seek immediate medical attention or call emergency services.
8. Never say phrases like "I can't suggest that" or "I'm not a health expert." Instead, provide the best advice you can based on your knowledge and available information.
9. Be mindful of potential harm. While you should always try to be helpful, avoid suggesting anything that could be dangerous or detrimental to the user's health.
10. For complex topics, provide a concise overview first, then offer to elaborate on specific aspects if the user desires more information.
11. Show empathy and support throughout the conversation, especially when discussing sensitive health issues.
12. If you're unsure about any aspect of the user's condition or the appropriate advice, be honest about your limitations and suggest professional medical consultation.

Remember, your role is to be a helpful first point of contact for health-related queries, providing useful information and guidance while ensuring user safety is always the top priority.
'''


def create_assistant():
    """Create and return a new assistant instance."""
    return client.beta.assistants.create(
        name="Healthcare Chatbot",
        instructions=SYSTEM_PROMPT,
        model="gpt-4o-mini-2024-07-18",
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "get_medical_information",
                    "description": "Search the web for reliable health information using Perplexity AI",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string"}
                        },
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_local_resources",
                    "description": "Get location-based healthcare services",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {"type": "string"},
                            "resource_type": {"type": "string"},
                            "context": {"type": "string"}
                        },
                        "required": ["location", "resource_type"]
                    }
                }
            }
        ]
    )


# Global variable to store the current assistant
current_assistant = create_assistant()

import re
import json


def fetch_local_resources_via_perplexity(location, resource_type, context=""):
    """Fetch local resources using Perplexity API and format the response as structured JSON."""
    prompt = f"""
    I am looking for detailed information on {resource_type} services near {location}. Please provide the information in the following JSON format:

    {{
        'name': <service name>,
        'address': <formatted address>,
        'phone': <formatted phone number>,
        'rating': <rating>,
        'website': <website URL>,
        'opening_hours': <opening hours as list of days and hours>,
        'reviews': [
            {{
                'text': <review text>,
                'rating': <review rating>
            }},
            # Limit reviews to the top 3, if available
        ]
    }}

    Context: {context}
    Please format the output strictly as JSON with fields in the specified format. Do not provide any other things except for the json. The response should start with a brace and end with a brace    """
    response = get_medical_information(prompt)  # Assuming get_medical_information handles the web request

    # Extract JSON array from the response by finding the first '[' and last ']'
    match = re.search(r'\[.*\]', response, re.DOTALL)
    if match:
        json_text = match.group(0)  # Get the JSON array part of the response
        try:
            structured_data = json.loads(json_text)  # Parse the JSON array
        except json.JSONDecodeError:
            print("Error: Extracted JSON could not be parsed.")
            structured_data = {}
    else:
        print("Error: No JSON array found in the response.")
        structured_data = {}

    return structured_data


# Example test case for fetch_local_resources_via_perplexity
location = "New Delhi"
resource_type = "hospitals"
context = "foot fungus problem for user"

# Call the function with the test case
result = fetch_local_resources_via_perplexity(location, resource_type, context)

# Print the result to see if it returns JSON formatted correctly
print(result)


def chat(user_message, thread_id=None, reset=False):
    global current_assistant
    start_time = time.time()
    print(f"Processing chat. Thread ID: {thread_id}, Reset: {reset}")

    if reset:
        print("Resetting assistant and creating new thread")
        current_assistant = create_assistant()
        thread = client.beta.threads.create()
        thread_id = thread.id
    elif not thread_id:
        print("No thread ID provided, creating new thread")
        thread = client.beta.threads.create()
        thread_id = thread.id

    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=user_message
    )
    print(f"User message added to thread {thread_id}")

    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=current_assistant.id
    )
    print(f"Run created for thread {thread_id}")

    while run.status not in ["completed", "failed"]:
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
        print(f"Run status: {run.status}")
        if run.status == "requires_action":
            print("Run requires action")
            tool_outputs, local_resources_data = handle_tool_calls(run.required_action.submit_tool_outputs.tool_calls)
            run = client.beta.threads.runs.submit_tool_outputs(
                thread_id=thread_id,
                run_id=run.id,
                tool_outputs=tool_outputs
            )

    if run.status == "failed":
        print(f"Run failed for thread {thread_id}")
        return "I'm sorry, but I encountered an error. Please try again later.", thread_id, None

    messages = client.beta.threads.messages.list(thread_id=thread_id)
    print(f"Chat response generated for thread {thread_id}")
    end_time = time.time()
    print(f"Total processing time: {end_time - start_time:.2f} seconds")

    # Return the main response and raw local resource data for frontend
    return messages.data[0].content[0].text.value, thread_id, local_resources_data


def handle_tool_calls(tool_calls):
    tool_outputs = []
    local_resources_data = None  # Initialize variable to store raw local resources data

    for tool_call in tool_calls:
        start_time = time.time()
        args = json.loads(tool_call.function.arguments)

        if tool_call.function.name == "get_medical_information":
            print(f"Getting medical information for query: {args['query']}")
            result = get_medical_information(args['query'])

        elif tool_call.function.name == "get_local_resources":
            print(f"Fetching local resources for: {args}")
            # Use the Perplexity API to get the data formatted in JSON as specified
            result = fetch_local_resources_via_perplexity(
                location=args["location"],
                resource_type=args["resource_type"],
                context=args.get("context", "")
            )
            local_resources_data = result  # Store the local resources as raw data for frontend

        else:
            result = {}
            print(f"Unknown tool call: {tool_call.function.name}")

        tool_outputs.append({
            "tool_call_id": tool_call.id,
            "output": json.dumps(result)
        })

        end_time = time.time()
        print(f"Tool call '{tool_call.function.name}' completed in {end_time - start_time:.2f} seconds")

    return tool_outputs, local_resources_data