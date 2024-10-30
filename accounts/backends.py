from django.contrib.auth.backends import BaseBackend
from .models import Account

class AccountsBackend(BaseBackend):
    backend = 'accountsbackend'
    
    def authenticate(self, request, email = None, password = None):
        try:
            user = Account.objects.get(email = email)
        except Account.DoesNotExist:
            return None
            
        if user.check_password(password):
            return user
        
    def get_user(self, user_id):
        try:
            return Account.objects.get(pk = user_id)
        except Account.DoesNotExist:
            return None
