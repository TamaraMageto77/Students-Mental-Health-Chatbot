from django.urls import path
from .views import (
    chat_list_view,
    chat_detail_view,
    chat_create_view,
    chat_update_view,
    chat_delete_view,
    message_create_view,
    message_update_view,
    message_delete_view,
)

urlpatterns = [
    path('', chat_list_view, name='chats'),
    path('detail/<str:chat_id>/', chat_detail_view, name='chat_detail'),
    path('create/', chat_create_view, name='chat_create'),
    path('<str:chat_id>/update/', chat_update_view, name='chat_update'),
    path('<str:chat_id>/delete/', chat_delete_view, name='chat_delete'),
    path('<str:chat_id>/messages/create/', message_create_view, name='message_create'),
    path('<str:chat_id>/messages/<int:message_id>/update/', message_update_view, name='message_update'),
    path('<str:chat_id>/messages/<int:message_id>/delete/', message_delete_view, name='message_delete'),
]