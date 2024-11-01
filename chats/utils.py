import os
from ai21 import AI21Client
from ai21.models.chat import ChatMessage

os.environ["AI21_API_KEY"] = "UDkAKH55JEDTqUUhT4huRGNgjDMasWhv"

client = AI21Client()


def mental_health_chatbot(chat):
    # Prepare the messages list with the system message
    messages = [
        ChatMessage(
            role="system",
            content="You are a mental health assistant. You are helping a user with their mental health."
        )
    ]

    # Append previous messages to the messages list
    for message in chat.messages.all():
        role = "user" if message.type == "request" else "assistant"
        messages.append(ChatMessage(role=role, content=message.content))
        
    response = client.chat.completions.create(
        model="jamba-instruct-preview",  # Latest model
        messages=messages,
        temperature=0.8,
        max_tokens=200
    )
    return response.choices[0].message.content
