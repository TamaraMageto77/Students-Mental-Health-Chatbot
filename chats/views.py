from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from chats.utils import mental_health_chatbot
from .models import Chat, Message
from .forms import ChatForm, MessageForm
from django.http import JsonResponse
import json


@login_required
def chat_list_view(request):
    user_latest_chat = Chat.objects.filter(
        user=request.user).latest('timestamp')
    if user_latest_chat:
        return redirect('chat_detail', chat_id=str(user_latest_chat.id))
    return render(request, 'homepage.html')


@login_required
def chat_detail_view(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id, user=request.user)
    messages = chat.messages.all()
    return render(request, 'chat_detail.html', {'chat': chat, 'messages': messages})


@login_required
def chat_create_view(request):
    # create new chat for user and redirect to its detail view
    chat = Chat.objects.create(user=request.user)
    return redirect('chat_detail', chat_id=str(chat.id))


@login_required
def chat_update_view(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id, user=request.user)
    if request.method == 'POST':
        form = ChatForm(request.POST, instance=chat)
        if form.is_valid():
            form.save()
            return redirect('chat_detail', chat_id=chat.id)
    else:
        form = ChatForm(instance=chat)
    return render(request, 'chat_form.html', {'form': form})


@login_required
def chat_delete_view(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id, user=request.user)
    if request.method == 'POST':
        chat.delete()
        return redirect('chat_list')
    return render(request, 'chat_confirm_delete.html', {'chat': chat})


@login_required
def message_create_view(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id, user=request.user)
    if request.method == 'POST':
        data = json.loads(request.body)  # Read JSON data from the request
        message_content = data.get('message')
        # Save the message to the database
        # Ensure you save the message with a timestamp
        Message.objects.create(
            chat=chat, content=message_content)
        # Get the response from the chatbot
        response = mental_health_chatbot(message_content)
        # Save the response to the database
        response_message = Message.objects.create(
            chat=chat, content=response, type='response')
        return JsonResponse({
            'status': 'success',
            'message': response_message.content,  # Return the message content
            # Format the timestamp for display
            'time': response_message.timestamp.strftime('%I:%M %p'),
            'message_id': response_message.id
        }
        )
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)


@login_required
def message_update_view(request, chat_id, message_id):
    chat = get_object_or_404(Chat, id=chat_id, user=request.user)
    message = get_object_or_404(Message, id=message_id, chat=chat)
    if request.method == 'POST':
        form = MessageForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            return redirect('chat_detail', chat_id=chat.id)
    else:
        form = MessageForm(instance=message)
    return render(request, 'message_form.html', {'form': form})


@login_required
def message_delete_view(request, chat_id, message_id):
    chat = get_object_or_404(Chat, id=chat_id, user=request.user)
    message = get_object_or_404(Message, id=message_id, chat=chat)
    if request.method == 'POST':
        message.delete()
        return redirect('chat_detail', chat_id=chat.id)
    return render(request, 'message_confirm_delete.html', {'message': message})
