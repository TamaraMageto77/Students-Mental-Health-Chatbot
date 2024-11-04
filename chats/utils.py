import os
from ai21 import AI21Client
from ai21.models.chat import ChatMessage

os.environ["AI21_API_KEY"] = "NLO8wYhIMVW6uHUJeCWSI8kT4m7ZBn4O"

client = AI21Client()


def mental_health_chatbot(chat):
    # Prepare the messages list with the system message
    messages = [
        ChatMessage(
            role="system",
            content="""
            For mental health inquiries from students: You are a supportive therapist. Provide concise but complete responses that:
            1. Acknowledge the person's feelings
            2. Validate their experience
            3. Offer clear, practical support or next steps
            4. End with a specific question or supportive statement
            """
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
