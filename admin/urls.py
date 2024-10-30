from django.urls import path
from .views import homepage

urlpatterns = [
    path('', homepage, name='dashboard'),
    path('accounts/', homepage, name='admin_accounts'),
    
]