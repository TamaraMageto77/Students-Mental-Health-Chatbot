from django.db import models
from django.contrib.auth import get_user_model
import uuid
from django.urls import reverse

User = get_user_model()

# Create your models here.
class Chat(models.Model):
    """Model definition for Chat."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta definition for Chat."""
        verbose_name = 'Chat'
        verbose_name_plural = 'Chats'
        ordering = ['-timestamp']  # Order by latest first

    def __str__(self):
        """Unicode representation of Chat."""
        return f'Conversation with {self.user} at {self.timestamp}'
    
    def get_absolute_url(self):
        return reverse("chat_detail", kwargs={"chat_id": self.pk})
    

class Message(models.Model):
    """Model definition for Message."""
    MESSAGE_TYPE_CHOICES = [
        ('request', 'Request'),
        ('response', 'Response'),
        ('counselor', 'Counselor')
    ]
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    type = models.CharField(max_length=10, choices=MESSAGE_TYPE_CHOICES,default='request')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta definition for Message."""
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        ordering = ['timestamp']  # Order by latest first

    def __str__(self):
        """Unicode representation of Message."""
        return f'Message from {self.chat} at {self.timestamp}'