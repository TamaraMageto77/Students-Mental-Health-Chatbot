import os
from ai21 import AI21Client
from ai21.models.chat import ChatMessage


os.environ["AI21_API_KEY"] = "B1XGOtKyKcH9qhKqSa8pwAMwnRskSmTX"

client = AI21Client()

def mental_health_chatbot(chat):
    # Get the latest user message
    latest_message = chat.messages.order_by('-timestamp').first()
    user_message = latest_message.content

    # Define mental health keywords
    mental_health_keywords = [
        "anxiety", "depression", "stress", "emotion", "feeling", "mental health",
        "therapy", "counseling", "sad", "happy", "overwhelmed", "panic", "mood"
    ]

    # Create a system prompt for intent detection
    intent_prompt = f"""
    Determine if the following message is related to mental health based on these keywords: {', '.join(mental_health_keywords)}.
    Message: "{user_message}"
    Respond with "Yes" if it is related, or "No" if it is not.
    """

    # Use the AI model to classify the intent
    intent_response = client.chat.completions.create(
        model="jamba-1.5-large",
        messages=[ChatMessage(role="user", content=intent_prompt)],
        max_tokens=1,
        temperature=0
    )
    intent = intent_response.choices[0].message.content.strip()

    if intent.lower() == "yes":
        # Proceed with the chat as usual
        messages = [
            ChatMessage(
                role="system",
                content="""
                You are a mental health support counselor who ONLY responds to mental health and emotional wellbeing inquiries.
                For mental health questions:
                1. Validate feelings with a brief acknowledgment
                2. Normalize their experience
                3. Offer 1-2 practical next steps or coping strategies
                4. Close with a supportive statement or gentle follow-up question

                For ANY non-mental health topics, respond only with:
                "I'm a mental health counselor and can only provide support for mental health concerns. For questions about [topic], please seek assistance from an appropriate specialist."

                Key boundaries:
                - Only discuss mental health and emotional wellbeing
                - No medical advice or diagnoses
                - No academic, relationship, career or other general life advice
                - Refer to crisis services when appropriate
                - Encourage professional help for serious concerns
                """
            )
        ]

        # Append previous messages to the messages list
        for message in chat.messages.all():
            role = "user" if message.type == "request" else "assistant"
            messages.append(ChatMessage(role=role, content=message.content))

        response = client.chat.completions.create(
            model="jamba-instruct-preview",
            messages=messages,
            temperature=0.8,
            max_tokens=200
        )
        return response.choices[0].message.content
    else:
        # Return a custom response for non-mental health topics
        return "I'm a mental health counselor and can only provide support for mental health concerns. For questions about other topics, please seek assistance from an appropriate specialist."