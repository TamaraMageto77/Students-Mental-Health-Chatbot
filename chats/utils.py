import os
from ai21 import AI21Client
from ai21.models.chat import ChatMessage

os.environ["AI21_API_KEY"] = "UDkAKH55JEDTqUUhT4huRGNgjDMasWhv"

client = AI21Client()

def mental_health_chatbot(prompt_text):
    response = client.chat.completions.create(
        model="jamba-instruct-preview",  # Latest model
        messages=[ChatMessage(
            role="assistant",
            content=prompt_text
        )],
        temperature=0.8,
        max_tokens=200
    )
    return response.choices[0].message.content
